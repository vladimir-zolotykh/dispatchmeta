#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import MutableMapping
from types import MethodType
from inspect import signature, _empty
from functools import wraps


class Method:
    def __init__(self, name: str):  # name: method name
        self.name = name
        self.methods = {}

    def register(self, func):
        sig = signature(func)
        typ = tuple()
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            if parm.annotation is _empty:
                raise TypeError("{}: Missed annotation")
            if parm.default is not _empty:
                self.methods[typ] = func
            typ = typ + (parm.annotation,)
        self.methods[typ] = func

    def __get__(self, instance, owner):
        return MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        typ = tuple(type(a) for a in args[1:])
        return self.methods[typ](*args, **kwargs)


class MultiDict(dict):
    def __setitem__(self, key, value):
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, value)
        else:
            mm = self.setdefault(key, Method(key))
            mm.register(value)


class MultiMeta(type):
    @classmethod
    def __prepare__(mcls, clsname, bases, /, **kwargs) -> MutableMapping:
        return MultiDict()


def show_types(func):
    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        args1 = []
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            if parm.default is not _empty and name not in bound.arguments:
                args1.append(parm.annotation.__name__ + f"[{parm.default}]")
            else:
                args1.append(parm.annotation.__name__)
        sargs = "-".join(args1)
        pname = f"{func.__name__}-{sargs}"
        print(f"{pname}{args[1:]}")
        res = func(*args, **kwargs)
        return res

    return wrapper


class Box(metaclass=MultiMeta):
    @show_types
    def add(self, x: int, y: int) -> int:
        return x + y

    @show_types
    def add(self, x: float, y: float = 7.6) -> float:  # noqa: F811
        return x + y

    @show_types
    def add(self, x: str, y: str) -> str:  # noqa: F811
        return x + y


if __name__ == "__main__":
    box = Box()
    print(box.add(3, 4))
    print(box.add(3.3, 4.4))
    print(box.add(3.3))
    print(box.add("3.3", "4.4"))
