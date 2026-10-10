#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Node:
    pass


class Stop(Node):
    def __init__(self, n):
        self.n = n


class Add(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b


def fib_node(n) -> Node:
    if n < 2:
        return Stop(n)
    else:
        return Add(fib_node(n - 2), fib_node(n - 1))
