from collections import Counter
from functools import partial
from operator import attrgetter
from typing import Iterable, Iterator

from lark import Lark, LarkError

from .types import Design, Flower, FlowerCounter


def create_design(parser: Lark, design: str) -> Design:
    try:
        tree = parser.parse(design)
    except LarkError as exc:
        raise ValueError(f"Bad design syntax in {design!r}") from exc
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
        tree = parser.parse(flower)
    except LarkError as exc:
        raise ValueError(f"Bad flower syntax in {flower!r}") from exc
    return Flower(*map(str, tree.children))


def generate_flowers(flowers: Iterable[str]) -> Iterator[Flower]:
    """Yields parsed Flowers from an iterable of flower specifications."""
    parser = get_parser("flower")
    return map(partial(create_flower, parser), flowers)


def generate_designs(designs: Iterable[str]) -> Iterator[Design]:
    """Yields parsed Designs from an iterable of design specifications."""
    parser = get_parser("design")
    return map(partial(create_design, parser), designs)


def get_parser(start: str) -> Lark:
    """Creates an LALR parser from the balderdash grammar with given start."""
    return Lark.open("balderdash.lark", parser="lalr", start=start, rel_to=__file__)
