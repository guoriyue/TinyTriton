"""Run the checks for the currently published lesson."""

import argparse
import os
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="TinyTriton Step 1")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="check your Step 1 implementation")
    check.add_argument("step", nargs="?", choices=["step01"], default="step01")
    check.add_argument("--solution", action="store_true")
    options, extra = parser.parse_known_args(argv)
    folder = "solutions" if options.solution else "problems"
    path = Path(os.environ.get("TINYTRITON_COMPILER", f"{folder}/step01.py")).resolve()
    if not path.is_file():
        parser.error(f"no compiler at {path}; run from the repository root")
    import pytest

    return pytest.main(
        [
            str(Path(__file__).with_name("checks.py")),
            f"--compiler-path={path}",
            *extra,
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
