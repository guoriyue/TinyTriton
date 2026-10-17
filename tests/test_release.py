"""Regression checks for lesson selection and sibling import isolation."""

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest


def test_step01_command_does_not_select_interpreter_checks():
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ)
    environment.pop("TINYTRITON_COMPILER", None)
    result = subprocess.run(
        [sys.executable, "-m", "tinytriton.cli", "check", "step01", "--solution", "-v"],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "test_step01_records_dependencies" in result.stdout
    assert "test_step02_vector_add" not in result.stdout


def test_step02_command_includes_its_prerequisite():
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ)
    environment.pop("TINYTRITON_COMPILER", None)
    result = subprocess.run(
        [sys.executable, "-m", "tinytriton.cli", "check", "step02", "--solution", "-v"],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "test_step01_records_dependencies" in result.stdout
    assert "test_step02_vector_add" in result.stdout


def test_loading_a_learner_does_not_reuse_a_cached_reference(tmp_path):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "lesson_loader_test", root / "src/tinytriton/conftest.py"
    )
    fixtures = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixtures)

    def request_for(path):
        return SimpleNamespace(config=SimpleNamespace(getoption=lambda key: str(path)))

    reference = fixtures.compiler.__wrapped__(request_for(root / "solutions/step02.py"))
    assert callable(reference.run)
    (tmp_path / "step01.py").write_text(
        'class Compiler:\n    def parse(self, text):\n        raise RuntimeError("learner")\n'
    )
    (tmp_path / "step02.py").write_text(
        "import step01\nclass Compiler(step01.Compiler):\n    pass\n"
    )
    learner = fixtures.compiler.__wrapped__(request_for(tmp_path / "step02.py"))
    with pytest.raises(RuntimeError, match="learner"):
        learner.parse("unused")
