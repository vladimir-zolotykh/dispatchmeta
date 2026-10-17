#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import warnings
import pytest


class BunchMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        defaults = {}

        def __init__(self, **kwargs):
            for key in defaults:
                if key in kwargs:
                    setattr(self, key, kwargs[key])
                    del kwargs[key]
                else:
                    setattr(self, key, defaults[key])
            if kwargs:
                warnings.warn(f"{', '.join(list(kwargs))}: no matching slots found")

        def __repr__(self):
            mod = []
            for key in defaults:
                val = getattr(self, key)
                if val != defaults[key]:
                    mod.append(key)
            args = ", ".join(f"{key}={getattr(self, key)!r}" for key in mod)
            return f"{type(self).__name__}({args})"

        ns = dict(__slots__=[], __init__=__init__, __repr__=__repr__)
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                if key in ns:
                    raise TypeError(f"{key}: not allowed to overwrite")
                ns[key] = val
            else:
                ns["__slots__"].append(key)
                defaults[key] = val
        return super().__new__(mcls, clsname, bases, ns)


class Person(metaclass=BunchMeta):
    name = "Bob"
    age = 37
    salary = 1200


def test_person(capsys):
    assert str(Person()) == "Person()"
    assert str(Person(age=38)) == "Person(age=38)"


def test_person_no_matching_slots():
    with pytest.warns(UserWarning, match="job: no matching slots found"):
        Person(job="Senior Java Developer")


def test_person_no_attribute():
    p = Person()
    with pytest.raises(
        AttributeError, match="'Person' object has no attribute 'gender'"
    ):
        p.gender = "male"


def test_person_no_overwrite():
    with pytest.raises(TypeError, match="__repr__: not allowed to overwrite"):

        class Person(metaclass=BunchMeta):
            age = 37

            def __repr__(self):
                pass


if __name__ == "__main__":
    test_person_no_overwrite()
