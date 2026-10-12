#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
from types import MethodType
import math


class lazyproperty:
    def __init__(self, func: Callable):
        self._func = func

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self._func, instance)


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print("calculating area")
        return math.pi * self.radius**2

    @lazyproperty
    def circumference(self):
        print("calculating circumference")
        return 2 * math.pi * self.radius


def test_circle():
    c = Circle(10.2)
    print("{:.2f}".format(c.area()))
    print("{:.2f}".format(c.circumference()))


if __name__ == "__main__":
    test_circle()
