#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Literal, get_origin, get_args
import re
from functools import wraps
from inspect import signature, _empty
import pytest


def autoassert(func):
    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, parm in sig.parameters.items():
            if (anno := parm.annotation) is not _empty:
                if get_origin(anno) is Literal:
                    lit = get_args(anno)
                    typ = tuple(type(x) for x in lit)
                    val = bound.arguments[name]
                    if not isinstance(val, typ):
                        raise TypeError(
                            f"{name!r} must by of types {tuple(typ.__name__ for typ in typ)}"
                            f", got type {type(val).__name__}"
                        )
                    if val not in lit:
                        raise ValueError(f"{name!r} must be one of {lit}")
                elif not isinstance(bound.arguments[name], anno):
                    raise TypeError(f"{name!r} must be of type {anno}")
        res = func(*args, **kwargs)
        return res

    return wrapper


@autoassert
def move(src: int, dst: int):
    print(src, dst)


@autoassert
def move2(src: int, dst: Literal[0, 1, 2]):
    print(src, dst)


def test_autoassert():
    move(0, 2)
    with pytest.raises(TypeError, match="'dst' must be of type <class 'int'>"):
        move(1, "a")
    with pytest.raises(ValueError, match=re.escape("'dst' must be one of (0, 1, 2)")):
        move2(1, 3)
    with pytest.raises(
        TypeError,
        match=re.escape("'dst' must by of types ('int', 'int', 'int'), got type str"),
    ):
        move2(0, "A")


if __name__ == "__main__":
    move2(0, "A")
