from dataclasses import dataclass
from enum import auto, Enum
from typing import Any, Generator

from Parser import TreeNode,BinOp, Int, Float, UnaryOp, Program, ExprStatement

type BytecodeGenerator = Generator[Bytecode, None, None]

class BytecodeType(Enum):
    BINOP = auto()
    UNARYOP = auto()
    PUSH = auto()
    POP = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

@dataclass
class Bytecode:
    type: BytecodeType
    value: Any = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type.name}, {self.value!r})"

class Compiler:
    def __init__(self, tree: TreeNode) -> None:
        self.tree = tree

    def compile(self) -> BytecodeGenerator:
        return self._compile(self.tree)

    def _compile(self, tree: TreeNode) -> BytecodeGenerator:
        match tree:
            case BinOp(op, left, right):
                yield from self._compile(left)
                yield from self._compile(right)
                yield Bytecode(BytecodeType.BINOP, op)
            case Int(value):
                yield Bytecode(BytecodeType.PUSH, value)
            case Float(value):
                yield Bytecode(BytecodeType.PUSH, value)
            case UnaryOp(op, value):
                yield from self._compile(value)
                yield Bytecode(BytecodeType.UNARYOP, op)

    def compile_UnaryOp(self, tree: UnaryOp) -> BytecodeGenerator:
        yield from self._compile(tree.value)
        yield Bytecode(BytecodeType.UNARYOP, tree.op)

    def compile_Program(self, program: Program) -> BytecodeGenerator:
        for statement in program.statements:
            yield from self._compile(statement)

    def compile_ExprStatement(self, expression: ExprStatement) -> BytecodeGenerator:
        yield from self._compile(expression.expr)
        yield Bytecode(BytecodeType.POP)

if __name__ == "__main__":
    from tokenizer import Tokenizer
    from Parser import Parser

    compiler = Compiler(Parser(list(Tokenizer("3 + 5 - 7 + 1.2 + 2.4 - 3.6"))).parse_computation())
    bytecode_generator = compiler.compile()
    for bc in bytecode_generator:
        print(bc)