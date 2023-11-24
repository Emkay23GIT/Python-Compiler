from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Generator
from string import digits

class TokenType(Enum):
    INT = auto()
    PLUS = auto()
    MINUS = auto()
    EOF = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

@dataclass
class Token:
    type: TokenType
    value: Any = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type!r}, {self.value!r})"

class Tokenizer:
    def __init__(self, code: str)-> None:
        self.code = code
        self.ptr: int = 0

    def next_token(self) -> Token:
        while self.ptr < len(self.code) and self.code[self.ptr] == " ":
            self.ptr += 1
        
        if self.ptr == len(self.code):
            return Token(TokenType.EOF)

        char = self.code[self.ptr]
        # self.ptr += 1 # we remove this from here.
        if char == "+":
            self.ptr += 1 # And add it here.
            return Token(TokenType.PLUS)
        elif char == '-':
            self.ptr += 1 # And here too.
            return Token(TokenType.MINUS)
        elif char in digits:
            integer = self.consume_int()  # If we found a digit, consume an integer.
            return Token(TokenType.INT, int(char))
        else:
            raise RuntimeError(f"Can't tokenize {char!r}.")
        
    def __iter__(self) -> Generator[Token, None, None]:
        while (token := self.next_token()).type != TokenType.EOF:
            yield token
        yield token # Yield  thE EOF token too.

    def consume_int(self) -> int:
        """Reads an integer from the source code."""
        start = self.ptr
        while self.ptr < len(self.code) and self.code[self.ptr] in digits:
            self.ptr += 1
        return int(self.code[start : self.ptr])


if __name__ == "__main__":
    code = "1 + 2 + 3 + 4 - 5 - 6 - 7 - 8"
    tokenizer = Tokenizer(code)
    print(code)
    for tok in tokenizer:
        print(f"\t{tok.type}, {tok.value}")

