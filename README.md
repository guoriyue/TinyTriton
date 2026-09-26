# TinyTriton: build a compiler, one step at a time

A tutorial series for Python programmers with no compiler background.
**Currently published: Step 1 — source code to instructions.**
Later lessons and implementations will arrive alongside their posts.

- [Series overview](https://guoriyue.github.io/blog/tinytriton-series/)
- [Step 1 blog](https://guoriyue.github.io/blog/tinytriton-step-1/)
- [Step 1 tutorial](steps/step01-triton-ir.md)
- [Exercise](https://github.com/guoriyue/TinyTriton/blob/main/problems/step01.py)
- [Reference implementation — try the exercise first](https://github.com/guoriyue/TinyTriton/blob/main/solutions/step01.py)

## Start

Python 3.10 or newer is enough. No GPU, CUDA, LLVM, or Triton installation is needed.

```bash
git clone https://github.com/guoriyue/TinyTriton.git
cd TinyTriton
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
tinytriton check step01
```

The unfinished exercise raises `NotImplementedError`; that is the expected starting
point. Implement its three TODOs using the tutorial, then rerun the check.
On Windows, activate the environment with `.venv\Scripts\activate` instead.

After attempting the exercise:

```bash
tinytriton check step01 --solution
```

The checks cover representation and dependencies, not execution on real arrays.
Execution will be the next lesson. The package contains only the sample source and
check runner; the compiler you write lives in `problems/step01.py`.

This is an educational Triton-style language, not the official Triton compiler.
This repository starts with Step 1; later lessons will be added as they are published.
License: [MIT](https://github.com/guoriyue/TinyTriton/blob/main/LICENSE).
