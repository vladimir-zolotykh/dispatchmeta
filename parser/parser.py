#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, Any
import operator
import re
import pytest


class Node:
    _masterpat: list[str] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "pat"):
            Node._masterpat.append(f"(?P<{cls.__name__}>{cls.pat})")


class Num(Node):
    pat = r"\d+"

    def __init__(self, val: float):
        pass


class BinOp(Node):
    def __init__(self, left: Node, right: Node) -> Node:
        self.left = left
        self.right = right


class Plus(BinOp):
    op = operator.add
    pat = r"\+"


class Minus(BinOp):
    op = operator.sub
    pat = r"\-"


class Mul(BinOp):
    op = operator.mul
    pat = r"\*"


class Div(BinOp):
    op = operator.truediv
    pat = r"/"


class Lparen(Node):
    pat = r"\("


class Rparen(Node):
    pat = r"\)"


class Ws(Node):
    pat = r"\s+"


class Token:
    def __init__(self, sym: str, val: Any = None):
        self.sym = sym
        self.val = val

    def __repr__(self):
        return "{}({})".format(self.sym, self.val if self.val else "")


def iter_tokens(sexpr: str) -> Iterator[Token]:
    masterpat = "|".join(Node._masterpat)
    for match in re.finditer(masterpat, sexpr):
        cls = globals()[match.lastgroup]
        if cls is not Ws:
            yield Token(cls, match.group(1))


class Parser:
    def __init__(self):
        self.tokens = None
        self.tok = None

    def parse(self, sexpr: str = "") -> Node:
        self.tokens = iter_tokens(sexpr)
        self._advance()
        return self.expr()

    def expr(self) -> Node:
        res = self.term()
        while self.tok and (op := self.tok.sym) in (Plus, Minus):
            self._consume()
            res = op(res, self.term())
        return res

    def term(self) -> Node:
        res = self.factor()
        while self.tok and (op := self.tok.sym) in (Mul, Div):
            self._consume()
            res = op(res, self.factor())
        return res

    def factor(self) -> Node:
        if self.tok.sym is Lparen:
            self._consume()
            res = self.expr()
            self._expect(Rparen)
        else:
            res = Num(self.tok.val)
            self._consume()
        return res

    def _advance(self) -> Token:
        self.tok = next(self.tokens, None)
        return self.tok

    def _expect(self, expected) -> None:
        if self.tok is not expected:
            raise SyntaxError(f"Expected {expected!r}, got {self.tok!r}")
        self._consume()

    def _consume(self) -> None:
        next(self.tokens, None)


def test_tokens():
    # print("|".join(Node._masterpat))
    sexpr = "2 + (3 * 4) + 5"
    for tok in iter_tokens(sexpr):
        print(tok)


def test_parser():
    sexpr = "2 + (3 * 4) + 5"
    n = Parser().parse(sexpr)
    print(n)


if __name__ == "__main__":
    test_parser
