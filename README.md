# TinyTriton. Build a compiler one step at a time

A tutorial series for Python programmers with no compiler background.
The first two lessons are published. Later lessons arrive with their articles.

| Lesson | Tutorial | Article | Exercise | Reference |
|---|---|---|---|---|
| 1. Source to instructions | [Read](steps/step01-triton-ir.md) | [Blog](https://guoriyue.github.io/blog/tinytriton-step-1/) | [step01.py](problems/step01.py) | [step01.py](solutions/step01.py) |
| 2. Execute the instructions | [Read](steps/step02-interpreter.md) | [Blog](https://guoriyue.github.io/blog/tinytriton-step-2/) | [step02.py](problems/step02.py) | [step02.py](solutions/step02.py) |

[Series overview](https://guoriyue.github.io/blog/tinytriton-series/)

## Start

Python 3.10 or newer is sufficient. NumPy supplies CPU array operations.
No GPU, CUDA, LLVM, or official Triton installation is required for these lessons.

```bash
git clone https://github.com/guoriyue/TinyTriton.git
cd TinyTriton
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
tinytriton check step01
```

On Windows, activate the environment with `.venv\Scripts\activate`.
An unfinished exercise raises `NotImplementedError`, which is the expected
starting point. Implement the three Step 1 methods before starting Step 2.

```bash
tinytriton check step02
```

Step 2 imports your Step 1 implementation. Its check runs both the representation
contracts and the CPU execution cases. It covers partial tiles, fallback values,
repeated invocations, and inactive output positions.

After attempting the exercise, compare the supplied references explicitly.

```bash
tinytriton check step01 --solution
tinytriton check step02 --solution
```

`tinytriton check` without a lesson keeps the original Step 1 default.
The package supplies source examples and the check runner. The learner compiler
lives in `problems`, and worked implementations live in `solutions`.

This is an educational language inspired by Triton. It is not the official
Triton compiler. Later lessons introduce GPU execution separately.

[MIT license](LICENSE)
