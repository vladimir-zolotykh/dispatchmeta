#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
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
