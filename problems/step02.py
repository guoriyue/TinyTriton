"""Step 2: interpret it.

It builds on your Step 1: `import step01` is problems/step01.py.
Everything here but the TODOs is given. Write: execute, evaluate.

Before coding, read the parameter conventions, then the state contracts:
    steps/step02-interpreter.md#from-a-parameter-description-to-a-runtime-value
    steps/step02-interpreter.md#before-the-todos-objects-and-state

    tinytriton check step02
"""

import numpy as np

import step01


class Compiler(step01.Compiler):
    def run(self, program, arguments, grid):
        """Execute the Triton IR on NumPy arrays; grid is the number of programs."""
        for program_id in range(grid):
            self.execute(program, arguments, program_id)

    def execute(self, program, arguments, program_id):
        """Bind inputs, then execute instructions.

        Given convention: Value("x", "ptr") becomes self.values["x"] =
        ("x", 0), meaning element 0 of self.arguments["x"]. Keep the array
        itself in self.arguments. Value("n", "int") instead becomes the
        supplied number arguments["n"]. The lesson traces both cases before
        this TODO; no new record class is needed.
        """
        # Walkthrough: steps/step02-interpreter.md#from-a-parameter-description-to-a-runtime-value
        # TODO(Step 2): Remember arguments and program_id, bind each parameter in
        # self.values (a pointer is (array name, 0)), then evaluate every
        # instruction in order and bind its result.
        raise NotImplementedError("Step 2: execute")

    def evaluate(self, instr, a):
        """The value of one instruction, given the values of its arguments."""
        # Walkthrough: steps/step02-interpreter.md#from-a-parameter-description-to-a-runtime-value
        # TODO(Step 2): Return the NumPy value of one instruction. addptr adds to the
        # pointer's index. load and store obey the mask: inactive lanes must not access
        # their invalid target addresses or write to memory.
        raise NotImplementedError("Step 2: evaluate")
