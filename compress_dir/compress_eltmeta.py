#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class EltMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        fields = clsdict.get("_fields", [])
        for k, name in enumerate(fields):

            def getk(self, x=k):
                return self[x]

            def setk(self, val, x=k):
                self[x] = val

            setattr(cls, name, property(getk, setk))


class Elt(list, metaclass=EltMeta):
    _fields = ["cnt", "val"]


ComprType = list[int | Elt]


def merge(res, elt: Elt) -> ComprType:
    if isinstance(elt, Elt):
        if elt.cnt > 1:
            return res + [elt]
        else:
            return res + [elt.val]
    else:
        return res + [elt]


def compr(lst: list[int], elt: Elt = Elt(), res: ComprType = []) -> ComprType:
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


if __name__ == "__main__":
    print(compr([1, 1, 1, 0, 1, 0, 0, 0, 0, 1]))
