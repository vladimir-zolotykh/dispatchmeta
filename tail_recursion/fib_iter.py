#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def fib_iter(n):
    res = {0: 0, 1: 1}
    k = 2
    while k <= n:
        res[k] = res[k - 2] + res[k - 1]
        k += 1
    return res[n]


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
    assert fib_iter(n) == res
