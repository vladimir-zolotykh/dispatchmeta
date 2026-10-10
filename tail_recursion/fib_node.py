#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class Node:
    pass


class Stop(Node):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return f"{self.n}"

    def eval(self):
        return self.n


class Add(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"Add({repr(self.a)}, {repr(self.b)})"

    def eval(self):
        return self.a.eval() + self.b.eval()


def fib_node(n) -> Node:
    if n < 2:
        return Stop(n)
    else:
        return Add(fib_node(n - 2), fib_node(n - 1))


if __name__ == "__main__":
    n = fib_node(5)
    print(n)


@pytest.mark.parametrize(
    "n, res",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
    ],
)
def test_fib(n, res):
    assert fib_node(n).eval() == res
