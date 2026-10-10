#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Node:
    pass


class Stop(Node):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return f"{self.n}"


class Add(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"Add({repr(self.a)}, {repr(self.b)})"


def fib_node(n) -> Node:
    if n < 2:
        return Stop(n)
    else:
        return Add(fib_node(n - 2), fib_node(n - 1))


if __name__ == "__main__":
    n = fib_node(5)
    print(n)
