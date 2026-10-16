#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import warnings


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

        ns = dict(clsdict)
        for key, val in clsdict.items():
            if key in ("__init__", "__repr__"):
                raise TypeError(f"{key}: not allowed to overwrite")
            if key not in ("__module__", "__qualname__"):
                defaults[key] = val
                del ns[key]
        ns["__init__"] = __init__
        ns["__repr__"] = __repr__
        ns["__slots__"] = defaults
        return super().__new__(mcls, clsname, bases, ns)


class Person(metaclass=BunchMeta):
    name = "Bob"
    age = 37
    salary = 1200

    # def __repr__(self):
    #     pass


def test_person():
    assert str(Person()) == "Person()"
    assert str(Person(age=38)) == "Person(age=38)"
    p = Person(job="Senior Java Developer")
    p.gender = "male"
    # p = Person(age=38)
    # Person(position="Senior Pyrhon engineer")


if __name__ == "__main__":
    test_person()
