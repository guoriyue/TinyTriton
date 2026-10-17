"""Load the learner's file, or the explicitly requested reference file."""

import importlib.util
import sys
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--compiler-path", default="problems/step01.py")


@pytest.fixture
def compiler(request):
    path = request.config.getoption("--compiler-path")
    path = Path(path).resolve()
    # Each lesson imports its predecessor by its sibling module name. Do not
    # reuse a cached solution when checking a learner file in the same process.
    for sibling in path.parent.glob("step[0-9][0-9].py"):
        sys.modules.pop(sibling.stem, None)
    spec = importlib.util.spec_from_file_location("compiler_under_test", path)
    module = importlib.util.module_from_spec(spec)
    # dataclasses consults the defining module while constructing records.
    sys.modules[spec.name] = module
    previous_path = list(sys.path)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = previous_path
    return module.Compiler()
