import operator
from typing import Any

from compiler import Bytecode, BytecodeType

BINOPS_TO_OPERATOR = {
    "**": operator.pow,
    "%": operator.mod,
    "/": operator.truediv,
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,
}
class Stack:
    def __init__(self) -> None:
        self.stack: list[float] = []

    def push(self, item: float) -> None:
        self.stack.append(item)

    def pop(self) -> float:
        return self.stack.pop()

    def peek(self) -> float:
        return self.stack[-1]

    def __repr__(self) -> str:
        return f"Stack({self.stack})"
    
class Interpreter:
    def __init__(self, bytecode: list[Bytecode]) -> None:
        self.stack = Stack()
        self.bytecode = bytecode
        self.ptr: int = 0
        self.last_value_popped: Any = None


    def interpret(self) -> None:
        while self.ptr < len(self.bytecode):
            bc = self.bytecode[self.ptr]
            bc_type = bc.type

            interpret_method = getattr(self, f"interpret_{bc_type.name}", None)
            if interpret_method is None:
                raise RuntimeError(f"Can't interpret {bc_type}.")

            interpret_method(bc)
            self.ptr += 1

        print("Done!")
        print(self.stack)

    def interpret_PUSH(self, bc: Bytecode) -> None:
        self.stack.push(bc.value)

    def interpret_POP(self, bc: Bytecode) -> None:
        self.last_value_popped = self.stack.pop()

    def interpret_BINOP(self, bc: Bytecode) -> None:
        result = self.stack.pop()
        if bc.value == "-":
            result = -result
        elif bc.value != "+":
            raise RuntimeError(f"Unknown unary operator {bc.value}.")
        self.stack.push(result)

    def interpret_UNARYOP(self, bc: Bytecode) -> None:
        result = self.stack.pop()
        if bc.value == "+":
            pass
        elif bc.value == "-":
            result = -result
        else:
            raise RuntimeError(f"Unknown operator {bc.value}.")
        self.stack.push(result)

if __name__ == "__main__":
    import sys

    from tokenizer import Tokenizer
    from Parser import Parser
    from compiler import Compiler
    
    if len(sys.argv) != 2:
        print("Usage: python your_script.py \"2 + 3\"")
        sys.exit(1)

    code = sys.argv[1]
    tokens = list(Tokenizer(code))
    tree = Parser(tokens).parse()
    bytecode = list(Compiler(tree).compile())
    Interpreter(bytecode).interpret()