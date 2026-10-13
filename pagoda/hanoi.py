#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from array import array

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


def solve(num_disks, src, dst, aux):
    if num_disks < 1:
        return
    solve(num_disks - 1, src, aux, dst)
    move(src, dst)
    solve(num_disks - 1, aux, dst, src)


if __name__ == "__main__":
    init_pegs(3)
    solve(3, 0, 2, 1)
    print(pegs)
