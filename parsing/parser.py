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


def iter_tokens(sexpr: str) -> Iterator[Token]:
    for match in re.finditer(masterpat, sexpr):
        if (name := match.lastgroup) != "WS":
            yield Token(name, match.group(0))


def test_iter_tokens(capsys):
    for tok in iter_tokens("2 + (3 * 4) + 5"):
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
        return f"{type(self).__name__}({repr(self.left)}, {repr(self.right)})"

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


class Parser:
    def __init__(self):
        self.tokens = None
        self.tok = None

    def parse(self, sexpr: str) -> Node:
        self.tokens = iter_tokens(sexpr)
        self._advance()
        return self.expr()

    def expr(self) -> Node:
        res = self.term()
        while self.tok and (op := self.tok.val) in ("+", "-"):
            self._consume()
            right = self.term()
            res = Plus(res, right) if op == "+" else Minus(res, right)
        return res

    def term(self) -> Node:
        res = self.factor()
        while self.tok and (op := self.tok.val) in ("*", "/"):
            self._consume()
            right = self.factor()
            res = Mul(res, right) if op == "*" else Div(res, right)
        return res

    def factor(self) -> Node:
        if self.tok.val == "(":
            self._consume()
            res = self.expr()
            self._consume()
        else:
            res = Num(float(self.tok.val))
            self._consume()
        return res

    def _advance(self) -> Token:
        self.tok = next(self.tokens, None)
        return self.tok

    def _consume(self) -> None:
        self.tok = next(self.tokens, None)

    def _expect(self, expected) -> None:
        if self.tok.name != expected.name:
            raise SyntaxError(f"Expected {expected}, got {self.tok.name}")
        self._consume()


if __name__ == "__main__":
    n: Node = Parser().parse("2 + (3 * 4) + 5")
    print(n)
