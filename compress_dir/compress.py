#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


def merge(res, elt):
    if isinstance(elt, list):
        if elt[0] > 1:
            return res + [elt]
        else:
            return res + [elt[1]]
    else:
        return res + [elt]


def compr(lst, elt=[], res=[]):
    if not lst:
        return merge(res, elt)
    else:
        car, *rest = lst
        if not elt:
            return compr(rest, [1, car], res)
        if elt[1] == car:
            elt[0] += 1
        else:
            res = merge(res, elt)
            elt = [1, car]
        return compr(rest, elt, res)


def compress(lst: list[int]) -> list[tuple[int, int] | int]:
    return compr(lst, [])


def decompress(lst: list[tuple[int, int] | int]) -> list[int]:
    pass
