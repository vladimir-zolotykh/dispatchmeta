#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import MutableMapping
from types import MethodType
from inspect import signature, _empty


class Method:
    def __init__(self, name: str):  # name: method name
        self.name = name
        self.methods = {}

    def register(self, func):
        sig = signature(func)
        typ = tuple()
        for name, parm in sig.parameters.items():
            if parm.annotation is _empty:
                raise TypeError("{}: Missed annotation")
            if name == "self":
                continue
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


class Box(metaclass=MultiMeta):
    def add(self, x: int, y: int) -> int:
        print("integer add")
        return x + y

    def add(self, x: float, y: float = 7.6) -> float:  # noqa: F811
        print("float add")
        return x + y

    def add(self, x: str, y: str) -> str:  # noqa: F811
        print("string add")
        return x + y


if __name__ == "__main__":
    box = Box()
    box.add(3, 4)
    box.add(3.3, 4.4)
    box.add(3.3)
    box.add("3.3", "4.4")
