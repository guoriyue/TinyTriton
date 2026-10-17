"""Step 2: interpret it.

Parameter conventions explained before this code: steps/step02-interpreter.md#from-a-parameter-description-to-a-runtime-value

Read execute -> evaluate: IR descriptions become runtime values in self.values.
Lesson checkpoints: steps/step02-interpreter.md#build-and-inspect-in-this-order
"""

import numpy as np

import step01


class Compiler(step01.Compiler):
    def run(self, program, arguments, grid):
        """Execute the Triton IR on NumPy arrays; grid is the number of programs."""
        for program_id in range(grid):
            self.execute(program, arguments, program_id)

    def execute(self, program, arguments, program_id):
        # Runtime state is separate from the frontend's source-name table.
        self.arguments = arguments
        self.program_id = program_id
        self.values = {}
        for parameter in program.params:
            if parameter.kind == "ptr":
                # Keep the array name and element offset; addptr updates the
                # offset, and load/store find the array in self.arguments.
                value = (parameter.name, 0)
            else:
                value = arguments[parameter.name]
            self.values[parameter.name] = value

        for instr in program.body:
            operands = [self.values[value.name] for value in instr.args]
            result = self.evaluate(instr, operands)
            if instr.result is not None:  # stores change memory, with no result
                self.values[instr.result.name] = result

    def evaluate(self, instr, a):
        """The value of one instruction, given the values of its arguments."""
        op = instr.op
        if op == "const":
            return instr.attrs["value"]
        if op == "program_id":
            return self.program_id
        if op == "arange":
            return np.arange(instr.attrs["start"], instr.attrs["end"])
        if op == "add":
            return a[0] + a[1]
        if op == "mul":
            return a[0] * a[1]
        if op == "lt":
            return a[0] < a[1]
        if op == "addptr":
            (base, index), offset = a
            return base, index + offset
        if op == "load":
            (base, index), mask, other = a
            memory = self.arguments[base].reshape(-1)
            # Inactive lanes read index 0 instead, then take `other`:
            # the mask must stop the read, not just replace the result.
            return np.where(mask, memory[np.where(mask, index, 0)], other)
        if op == "store":
            (base, index), value, mask = a
            self.arguments[base].reshape(-1)[index[mask]] = value[mask]
            return None
        raise NotImplementedError(op)
