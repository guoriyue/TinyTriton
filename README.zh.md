# TinyTriton. 一步一步编写编译器

面向会写 Python、但没有编译器基础的读者。当前已发布前两课。

| 课程 | 教程 | 练习 | 参考实现 |
|---|---|---|---|
| 第一课，将源码转换为指令 | [英文教程](steps/step01-triton-ir.md) | [step01.py](problems/step01.py) | [step01.py](solutions/step01.py) |
| 第二课，在 CPU 上执行指令 | [英文教程](steps/step02-interpreter.md) | [step02.py](problems/step02.py) | [step02.py](solutions/step02.py) |

第二课继承第一课的实现，增加 NumPy 解释器、模拟指针与带 mask 的内存访问。
这两课只需要 Python 3.10 或更新版本及 NumPy，不需要 GPU、CUDA、LLVM 或官方 Triton。
安装命令见 [README](README.md)。

```bash
python -m pip install -e '.[dev]'
tinytriton check step01
tinytriton check step02
```

第二课的检查也会运行第一课的检查。未完成 TODO 时出现 `NotImplementedError`
是预期现象。尝试练习后，可以使用 `--solution` 检查参考实现。

[系列总览](https://guoriyue.github.io/blog/tinytriton-series/)
