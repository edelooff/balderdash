from functools import partial
from collections import Counter
from operator import attrgetter
from typing import Iterable, Iterator

from lark import Lark, LarkError

from .types import Design, Flower, FlowerCounter


def create_design(parser: Lark, design: str) -> Design:
    try:
        tree = parser.parse(design, start="design")
    except LarkError as exc:
        raise ValueError("Bad design syntax") from exc
    name, size, *required_flowers, total_count = tree.children
    required: FlowerCounter = Counter()
    for count, species in map(attrgetter("children"), required_flowers):
        if (flower := Flower(str(species), str(size))) in required:
            raise ValueError(f"Multiple definitions of same required flower {flower}")
        required[flower] = int(count)
    if (additional := int(str(total_count)) - sum(required.values())) < 0:
        raise ValueError("Sum of required flowers greater than total size")
    return Design(str(name), str(size), required, additional)


def create_flower(parser: Lark, flower: str) -> Flower:
    try:
        tree = parser.parse(flower, start="flower")
    except LarkError as exc:
        raise ValueError("Bad flower syntax") from exc
    return Flower(*map(str, tree.children))


def generate_flowers(flowers: Iterable[str]) -> Iterator[Flower]:
    """Yields parsed Flowers from an iterable of flower specifications."""
    parser = Lark.open("design.lark", rel_to=__file__)
    return map(partial(create_flower, parser), flowers)


def generate_designs(designs: Iterable[str]) -> Iterator[Design]:
    """Yields parsed Designs from an iterable of design specifications."""
    parser = Lark.open("design.lark", rel_to=__file__)
    return map(partial(create_design, parser), designs)
