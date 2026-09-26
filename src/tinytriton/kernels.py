"""Source text for Step 1. Parsing this string does not execute it."""

vector_add = """def vector_add(x: ptr, y: ptr, out: ptr, n: int, BLOCK: tl.constexpr):
    offsets = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    mask = offsets < n
    a = tl.load(x + offsets, mask=mask, other=0.0)
    b = tl.load(y + offsets, mask=mask, other=0.0)
    tl.store(out + offsets, a + b, mask=mask)
"""
