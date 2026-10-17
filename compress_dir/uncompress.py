#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from copy import copy
from compress_eltmeta import Elt

ComprType = list[int | Elt]


def uncompr(zlst: ComprType, out: list[int] = []) -> list[int]:
    if not zlst:
        return out
    car, *rest = zlst
    if isinstance(car, Elt):
        for i in range(car.cnt):
            out += [car.val]
        return uncompr(rest, out)
    else:
        return uncompr(rest, out + [car])


def test_uncompr():
    assert uncompr([Elt([4, 0])]) == [0, 0, 0, 0]
    # assert uncompr([Elt([3, 1]), 0, 1, Elt([4, 0]), 1]) == [1, 1, 1, 0, 1, 0, 0, 0, 0, 1]


def test_uncompr2():
    res = uncompr([Elt([3, 1]), 0, 1, Elt([4, 0]), 1])
    assert copy(res) == [1, 1, 1, 0, 1, 0, 0, 0, 0, 1]


if __name__ == "__main__":
    print(uncompr([Elt([3, 1]), 0, 1, Elt([4, 0]), 1]))
