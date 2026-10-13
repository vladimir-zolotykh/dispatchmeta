#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from array import array
from collections import namedtuple
import pytest

Board = namedtuple("Board", ["num_disks", "src", "dst", "aux"])

pegs = [array("i"), array("i"), array("i")]


def init_pegs(num_disks: int = 3):
    pegs[0] = array("i", list(range(num_disks, 0, -1)))
    pegs[1] = array("i")
    pegs[2] = array("i")


def validate(b: Board):
    disk = pegs[b.src][-1]
    try:
        under = pegs[b.dst][-1]
    except IndexError:
        return
    if disk > under:
        raise ValueError(
            f"Cannot put disk {disk} (pegs[{b.src}]) over {under}  (pegs[{b.dst}])"
        )


def move(b: Board):
    validate(b)
    pegs[b.dst].append(pegs[b.src].pop())


def solve(b: Board):
    if b.num_disks < 1:
        return
    solve(Board(b.num_disks - 1, b.src, b.aux, b.dst))
    move(b)
    solve(Board(b.num_disks - 1, b.aux, b.dst, b.src))


@pytest.mark.parametrize(
    "num_disks, res",
    [
        (3, [array("i"), array("i"), array("i", [3, 2, 1])]),
        (4, [array("i"), array("i"), array("i", [4, 3, 2, 1])]),
        (5, [array("i"), array("i"), array("i", [5, 4, 3, 2, 1])]),
        (6, [array("i"), array("i"), array("i", [6, 5, 4, 3, 2, 1])]),
        (7, [array("i"), array("i"), array("i", [7, 6, 5, 4, 3, 2, 1])]),
        (8, [array("i"), array("i"), array("i", [8, 7, 6, 5, 4, 3, 2, 1])]),
    ],
)
def test_solve(num_disks, res):
    init_pegs(num_disks)
    solve(Board(num_disks, 0, 2, 1))
    assert pegs == res


if __name__ == "__main__":
    init_pegs(3)
    solve(Board(3, 0, 2, 1))
    print(pegs)
