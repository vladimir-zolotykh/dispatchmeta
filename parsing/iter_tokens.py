#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import operator
import re


class Token:
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def __str__(self):
        return self.val

    def __repr__(self):
        args = tuple(self.__dict__.values())
        return f"Token{args}"


TOKENS = {
    name: f"(?P<{name}>{pat})"
    for name, pat in {
        "LPAREN": r"\(",
        "RPAREN": r"\)",
        "PLUS": r"\+",
        "MINUS": r"-",
        "MUL": r"\*",
        "DIV": r"/",
        "NUM": r"\d+",
        "WS": r"\s+",
    }.items()
}
masterpat = "|".join(TOKENS.values())


def iter_token(sexpr: str) -> Iterator[Token]:
    for match in re.finditer(masterpat, sexpr):
        if (name := match.lastgroup) != "WS":
            yield Token(name, match.group(0))


if __name__ == "__main__":
    for tok in iter_token("2 + (3 * 4) + 5"):
        print(repr(tok))


def test_iter_tokens(capsys):
    for tok in iter_token("2 + (3 * 4) + 5"):
        print(repr(tok))
    # fmt: off
    assert (
        capsys.readouterr().out == """\
Token('NUM', '2')
Token('PLUS', '+')
Token('LPAREN', '(')
Token('NUM', '3')
Token('MUL', '*')
Token('NUM', '4')
Token('RPAREN', ')')
Token('PLUS', '+')
Token('NUM', '5')
"""
    )
    # fmt: on


class Node:
    pass


class Num(Node):
    def __init__(self, val: float):
        self.val = val

    def __repr__(self):
        return f"Num({self.val})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.val == other.val


class BinOp(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def __repr__(self):
        # tuple(repr(v) for v in d.values())
        return f"{type(self.__name__)}({repr(self.left)}, {repr(self.right)})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.__dict__ == other.__dict__


class Plus(BinOp):
    _op = operator.add


class Minus(BinOp):
    _op = operator.sub


class Mul(BinOp):
    _op = operator.mul


class Div(BinOp):
    _op = operator.truediv
