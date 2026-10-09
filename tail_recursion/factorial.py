#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def fact_rec(n):
    if n < 2:
        return 1
    else:
        return n * fact_rec(n - 1)


def fact_tail(n: int, res: int = 1) -> int:
    if n < 2:
        return res
    else:
        return fact_tail(n - 1, n * res)


def fact_iter(n):
    fac = 1
    i = 1
    for i in range(1, n + 1):
        fac *= i
    return fac


@pytest.mark.parametrize(
    "n, res",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (7, 5040),
        (8, 40320),
        (9, 362880),
    ],
)
def test_fact(n, res):
    assert fact_rec(n) == res
    assert fact_tail(n) == res
    assert fact_iter(n) == res
