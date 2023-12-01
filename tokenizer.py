from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Generator, Optional
from string import digits

class TokenType(Enum):
    INT = auto()
    FLOAT = auto()
    PLUS = auto()
    MINUS = auto()
    EOF = auto()
    LPAREN = auto()
    RPAREN = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    EXP = auto()
    NEWLINE = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

CHARS_AS_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "%": TokenType.MOD,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "**": TokenType.EXP,
    "/n": TokenType.EOF,
    "\n": TokenType.NEWLINE,  # Corrected the typo here
}

@dataclass
class Token:
    type: TokenType
    value: Any = None

class Tokenizer:
    def __init__(self, code: str)-> None:
        self.code = code 
        self.ptr: int = 0
        self.beginning_of_line = True

    def peek(self, length: int = 1) -> str:
        """Returns the substring that will be tokenized next."""
        substring = self.code[self.ptr : self.ptr + length] if self.ptr + length <= len(self.code) else ""
        return substring


    def next_token(self) -> Token:
        while self.ptr < len(self.code) and self.code[self.ptr] == " ":
            self.ptr += 1

        if self.ptr == len(self.code):
            return Token(TokenType.EOF)

        char = self.code[self.ptr]
        if char == "\n":
            self.ptr += 1
            if not self.beginning_of_line:
                self.beginning_of_line = True
                return Token(TokenType.NEWLINE)
            else:
                return self.next_token()

        self.beginning_of_line = False

        if self.peek(length=2) == "**":
            self.ptr += 2
            return Token(TokenType.EXP)

        char = self.code[self.ptr]

        if char in CHARS_AS_TOKENS:
            self.ptr += 1
            return Token(CHARS_AS_TOKENS[char])

        if char in digits or (char == "." and self.peek(2)[1] in digits):
            integer = self.consume_int()
            if self.ptr < len(self.code) and self.code[self.ptr] == ".":
                self.ptr += 1
                decimal = self.consume_decimal()
                if decimal:
                    float_str = f"{integer}.{decimal}"
                else:
                    float_str = f"{integer}."
                return Token(TokenType.FLOAT, float(float_str))
            return Token(TokenType.INT, int(integer))

        raise RuntimeError(f"Can't tokenize {char!r}.")

    def consume_decimal(self) -> float:
        """Reads a decimal part that starts with a . and returns it as a float."""
        start = self.ptr

        # Check if there are any digits after the decimal point
        has_digits = False
        while self.ptr < len(self.code) and self.code[self.ptr] in digits:
            has_digits = True
            self.ptr += 1

        # If no digits are found, return 0.0 as the decimal part
        if not has_digits:
            return 0.0

        decimal = self.code[start:self.ptr]

        # Handle the case of multiple consecutive dots
        dot_count = decimal.count(".")
        if dot_count > 1:
            raise RuntimeError(f"Invalid float format: {decimal}")

        # Handle the case where the decimal is at the end of the string
        if decimal.endswith("."):
            raise RuntimeError(f"Invalid float format: {decimal}")

        return float(decimal)



        
    def __iter__(self) -> Generator[Token, None, None]:
        while (token := self.next_token()).type != TokenType.EOF:
            yield token
        yield token # Yield  thE EOF token too.

    def consume_int(self) -> str:
        """Reads an integer from the source code."""
        start = self.ptr
        while self.ptr < len(self.code) and self.code[self.ptr] in digits:
            self.ptr += 1
        return self.code[start:self.ptr]



if __name__ == "__main__":
    code = "1 + .2 + 0.005 + 123.456 - .12 - 73. - 456 - 789"
    tokenizer = Tokenizer(code)
    print(code)
    for tok in tokenizer:
        print(f"\t{tok.type}, {tok.value}")

