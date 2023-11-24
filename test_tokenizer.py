import pytest
from tokenizer import Token, Tokenizer, TokenType

def  test_tokenizer_addition():
    tokens = list(Tokenizer("3 + 5"))
    assert tokens == [
 3),
        Token(TokenType.PLUS),
 5),
        Token(TokenType.EOF),
    ]

def test_tokenizer_subtraction():
    tokens = list(Tokenizer("3 - 6"))
    assert tokens == [
 3),
        Token(TokenType.MINUS),
 6),
        Token(TokenType.EOF),
    ]

def test_tokenizer_additions_and_subtractions():
    tokens = list(Tokenizer("1 + 2 + 3 + 4 - 5 - 6 + 7 - 8"))
    assert tokens == [
 1),
        Token(TokenType.PLUS),
 2),
        Token(TokenType.PLUS),
 3),
        Token(TokenType.PLUS),
 4),
        Token(TokenType.MINUS),
 5),
        Token(TokenType.MINUS),
 6),
        Token(TokenType.PLUS),
 7),
        Token(TokenType.MINUS),
 8),
        Token(TokenType.EOF),
    ]

def test_tokenizer_additions_and_subtractions_with_whitespaces():
    tokens = list(Tokenizer("   1+    2   +3+4-5 -  6 + 7 - 8     "))
    assert tokens == [
 1),
        Token(TokenType.PLUS),
 2),
        Token(TokenType.PLUS),
 3),
        Token(TokenType.PLUS),
 4),
        Token(TokenType.MINUS),
 5),
        Token(TokenType.MINUS),
 6),
        Token(TokenType.PLUS),
 7),
        Token(TokenType.MINUS),
 8),
        Token(TokenType.EOF),
    ]

def test_tokenizer_raises_error_on_garbage():
    with pytest.raises(RuntimeError):
        list(Tokenizer("$"))

@pytest.mark.parametrize(
    ["code", "token"],
    [
        ("+", Token(TokenType.PLUS)),
        ("-", Token(TokenType.MINUS)),
        ("3" 3)),
    ],
)

def test_tokenizer_recognises_each_token(code: str, token: Token):
    tokens = list(Tokenizer(code))
    assert tokens == [token, Token(TokenType.EOF)]

@pytest.mark.parametrize(
    ["code", "expected_value"],
    [
        (" 61      ", 61),
        ("    72345    ", 72345),
        ("9142351643", 9142351643),
        ("     642357413455672", 642357413455672),
    ],
)
def test_tokenizer_long_integers(code: str, expected_value: int):
    tokens = list(Tokenizer(code))
    assert [token.value for token in tokens[:-1]] == expected_value  # Compare only values, excluding EOF