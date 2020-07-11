from __future__ import annotations

import sys
from collections import Counter
from operator import attrgetter
from typing import Dict, NamedTuple

from lark import Lark, LarkError


class Design(NamedTuple):
    name: str
    size: str
    required: Dict[Flower, int]
    additional: int


class Flower(NamedTuple):
    species: str
    size: str


def create_design(parser: Lark, design: str) -> Design:
    try:
        tree = parser.parse(design, start="design")
    except LarkError as exc:
        raise ValueError("Bad design syntax") from exc
    name, size, *flower_trees, total_count = tree.children
    required: Dict[Flower, int] = Counter()
    for count, species in map(attrgetter('children'), flower_trees):
        if (flower := Flower(str(species), str(size))) in required:
            raise ValueError(f"Multiple definitions of same required flower {flower}")
        required[flower] = int(count)
    if (additional := int(str(total_count)) - sum(required.values())) < 0:
        raise ValueError("Sum of required flowers greater than total size")
    return Design(str(name), str(size), required, additional)


def main(*designs: str) -> None:
    """Parses commandline parameters into Designs using Lark parser."""
    parser = Lark.open("design.lark")
    for design in designs:
        print(create_design(parser, design))


if __name__ == "__main__":
    main(*sys.argv[1:])
