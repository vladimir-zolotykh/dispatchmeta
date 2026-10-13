#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import wraps
from inspect import signature, _empty
import pytest


def autoassert(func):
    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, parm in sig.parameters.items():
            if parm.annotation is not _empty:
                # assert isinstance(bound.arguments[name], parm.annotation)
                if not isinstance(bound.arguments[name], parm.annotation):
                    raise TypeError(f"{name} must be of type {parm.annotation}")
        res = func(*args, **kwargs)
        return res

    return wrapper


@autoassert
def move(src: int, dst: int):
    print(src, dst)


def test_autoassert():
    move(0, 2)
    with pytest.raises(TypeError, match="dst must be of type <class 'int'>"):
        move(1, "a")


if __name__ == "__main__":
    move(1, "a")
