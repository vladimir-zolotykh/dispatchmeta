#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Literal
from array import array
import pytest
from autoassert import autoassert

pegs = [array("i"), array("i"), array("i")]


def init_pegs(num_disks: int = 3):
    pegs[0] = array("i", list(range(num_disks, 0, -1)))
    pegs[1] = array("i")
    pegs[2] = array("i")


def validate(src: int, dst: int):
    disk = pegs[src][-1]
    try:
        under = pegs[dst][-1]
    except IndexError:
        return
    if disk > under:
        raise ValueError(
            f"Cannot put disk {disk} (pegs[{src}]) over {under}  (pegs[{dst}])"
        )


def move(src: int, dst: int):
    validate(src, dst)
    pegs[dst].append(pegs[src].pop())


@autoassert
def solve(
    num_disks: int, src: Literal[0, 1, 2], dst: Literal[0, 1, 2], aux: Literal[0, 1, 2]
):
    if num_disks < 1:
        return
    solve(num_disks - 1, src, aux, dst)
    move(src, dst)
    solve(num_disks - 1, aux, dst, src)


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
    solve(num_disks, 0, 2, 1)
    assert pegs == res


if __name__ == "__main__":
    init_pegs(3)
    solve(3, 0, 2, 1)
    print(pegs)
