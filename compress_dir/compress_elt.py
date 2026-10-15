#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import UserList


class Elt(UserList):
    @property
    def cnt(self):
        return self.data[0]

    @cnt.setter
    def cnt(self, val):
        self.data[0] = val

    @property
    def val(self):
        return self.data[1]

    @val.setter
    def val(self, val):
        self.data[1] = val


ComprType = list[int | Elt]


def merge(res: ComprType, elt: Elt) -> ComprType:
    if isinstance(elt, Elt):
        if elt.cnt > 1:
            return res + [elt]
        else:
            return res + [elt[1]]
    else:
        return res + [elt]


def compr(lst, elt=Elt(), res=[]):
    if not lst:
        return merge(res, elt)
    else:
        car, *rest = lst
        if not elt:
            return compr(rest, Elt((1, car)), res)
        if elt.val == car:
            elt.cnt += 1
        else:
            res = merge(res, elt)
            elt = Elt((1, car))
        return compr(rest, elt, res)


def test_compr():
    assert compr([1, 1, 1, 0, 1, 0, 0, 0, 0, 1]) == [[3, 1], 0, 1, [4, 0], 1]


if __name__ == "__main__":
    print(compr([1, 1, 1, 0, 1, 0, 0, 0, 0, 1]))
