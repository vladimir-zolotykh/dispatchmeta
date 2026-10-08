#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def fac_rec(n):
    if n < 2:
        return 1
    else:
        return n * fac_rec(n - 1)


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
def test_fac_rec(n, res):
    assert fac_rec(n) == res


def fac_tail(n: int, res: int = 1) -> int:
    if n < 2:
        return res
    else:
        return fac_tail(n - 1, n * res)


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
def test_fac_tail(n, res):
    assert fac_tail(n) == res
