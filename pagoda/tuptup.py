#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        fields = clsdict.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(n)))


class Tup(tuple, metaclass=TupMeta):
    def __new__(cls, *args, **kwargs):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Person(Tup):
    _fields = ["name", "age", "salary"]


def test_person():
    bob = Person("Bob", 37, 12000)
    assert (bob.name, bob.age, bob.salary) == ("Bob", 37, 12000)
    assert str(bob) == "('Bob', 37, 12000)"


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)
