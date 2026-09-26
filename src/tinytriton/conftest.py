"""Load the learner's file, or the explicitly requested reference file."""

import importlib.util
import sys

import pytest


def pytest_addoption(parser):
    parser.addoption("--compiler-path", default="problems/step01.py")


@pytest.fixture
def compiler(request):
    path = request.config.getoption("--compiler-path")
    spec = importlib.util.spec_from_file_location("step01_under_test", path)
    module = importlib.util.module_from_spec(spec)
    # dataclasses consults the defining module while constructing records.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.Compiler()
