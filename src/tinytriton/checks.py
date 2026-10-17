"""Check the published representation and CPU execution contracts."""

import ast

import numpy as np
import pytest

from tinytriton import kernels


def test_step01_parse_without_execution(compiler):
    function = compiler.parse(kernels.vector_add)
    assert isinstance(function, ast.FunctionDef)
    assert function.name == "vector_add"


@pytest.mark.parametrize("block", [4, 8])
def test_step01_records_dependencies_and_specialization(compiler, block):
    program = compiler.lower(compiler.parse(kernels.vector_add), block=block)
    assert program.name == "vector_add"
    assert [(p.name, p.kind, p.shape) for p in program.params] == [
        ("x", "ptr", ()),
        ("y", "ptr", ()),
        ("out", "ptr", ()),
        ("n", "int", ()),
    ]
    assert program.body
    assert str(program).strip()
    defined = {p.name: p for p in program.params}
    for instruction in program.body:
        for operand in instruction.args:
            assert operand.name in defined, "an operand must be defined before use"
            assert operand == defined[operand.name]
        if instruction.result is not None:
            assert instruction.result.name not in defined, "results need unique names"
            defined[instruction.result.name] = instruction.result
    ranges = [i for i in program.body if i.op == "arange"]
    assert len(ranges) == 1
    assert ranges[0].attrs == {"start": 0, "end": block}
    assert ranges[0].result.shape == (block,)
    loads = [i for i in program.body if i.op == "load"]
    assert len(loads) == 2
    for load in loads:
        assert load.result.kind == "float"
        assert load.result.shape == (block,)
        pointer, mask, other = load.args
        assert (pointer.kind, pointer.shape) == ("ptr", (block,))
        assert (mask.kind, mask.shape) == ("bool", (block,))
        assert (other.kind, other.shape) == ("float", ())
    store = program.body[-1]
    assert store.op == "store" and store.result is None
    assert [v.kind for v in store.args] == ["ptr", "float", "bool"]
    assert all(v.shape == (block,) for v in store.args)


def test_step01_expression_order_and_name_binding(compiler):
    program = compiler.lower(
        compiler.parse("def sample(a: int, b: int):\n    answer = a + b * 2\n"), block=4
    )
    result = compiler.env["answer"]
    producer = {i.result.name: i for i in program.body if i.result is not None}
    addition = producer[result.name]
    assert addition.op == "add"
    assert addition.args[0].name == "a"
    multiplication = producer[addition.args[1].name]
    assert multiplication.op == "mul"
    assert multiplication.args[0].name == "b"
    assert producer[multiplication.args[1].name].attrs["value"] == 2


def test_step01_each_compilation_starts_fresh(compiler):
    function = compiler.parse(kernels.vector_add)
    first = compiler.lower(function, block=4)
    first_body = list(first.body)
    second = compiler.lower(function, block=8)
    assert first is not second and first.body is not second.body
    assert first.body == first_body
    assert len(first.body) == len(second.body)


def test_step01_unknown_name_is_an_error(compiler):
    misspelled = kernels.vector_add.replace("* BLOCK", "* BLOKC")
    with pytest.raises(KeyError, match="BLOKC"):
        compiler.lower(compiler.parse(misspelled), block=4)


@pytest.mark.parametrize("n, block", [(1, 4), (4, 4), (6, 4), (6, 8), (10, 4)])
def test_step02_vector_add_and_untouched_tail(compiler, n, block):
    program = compiler.lower(compiler.parse(kernels.vector_add), block=block)
    x = np.arange(n, dtype=np.float32) * 3 + 100
    y = np.arange(n, dtype=np.float32) * 2 - 7
    out = np.full(n + block, -99, dtype=np.float32)
    result = compiler.run(
        program, {"x": x, "y": y, "out": out, "n": n}, (n + block - 1) // block
    )
    assert result is None
    np.testing.assert_array_equal(out[:n], x + y)
    np.testing.assert_array_equal(out[n:], -99)


def test_step02_load_returns_fallback_without_reading_invalid_targets(compiler):
    source = """def copy(x: ptr, out: ptr, n: int, BLOCK: tl.constexpr):
    offsets = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    values = tl.load(x + offsets, mask=offsets < n, other=7.0)
    tl.store(out + offsets, values, mask=offsets < 8)
"""
    program = compiler.lower(compiler.parse(source), block=4)
    x = np.array([100, 200, 300, 400, 500, 600], dtype=np.float32)
    out = np.full(8, -99, dtype=np.float32)
    compiler.run(program, {"x": x, "out": out, "n": 6}, grid=2)
    np.testing.assert_array_equal(out, [100, 200, 300, 400, 500, 600, 7, 7])


def test_step02_reuses_ir_with_fresh_invocation_arguments(compiler):
    program = compiler.lower(compiler.parse(kernels.vector_add), block=4)
    for n, start in [(6, 20), (4, 100)]:
        x = np.arange(n, dtype=np.float32) + start
        y = np.full(n, 10, dtype=np.float32)
        out = np.full(8, -99, dtype=np.float32)
        compiler.run(program, {"x": x, "y": y, "out": out, "n": n}, (n + 3) // 4)
        np.testing.assert_array_equal(out[:n], x + y)
        np.testing.assert_array_equal(out[n:], -99)


def test_step02_inactive_program_does_not_write(compiler):
    program = compiler.lower(compiler.parse(kernels.vector_add), block=4)
    x = np.arange(6, dtype=np.float32)
    y = np.full(6, 10, dtype=np.float32)
    out = np.full(12, -99, dtype=np.float32)
    compiler.run(program, {"x": x, "y": y, "out": out, "n": 6}, grid=3)
    np.testing.assert_array_equal(out[:6], x + y)
    np.testing.assert_array_equal(out[6:], -99)
