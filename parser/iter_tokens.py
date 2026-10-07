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
        if match.lastgroup != Ws.__name__:
            yield Token(match.lastgroup, match.group(1))


if __name__ == "__main__":
    # print("|".join(Node._masterpat))
    sexpr = "2 + (3 * 4) + 5"
    for tok in iter_tokens(sexpr):
        print(tok)
