from collections import Counter
from itertools import chain
from typing import Iterable, Iterator, TextIO

from .types import Bouquet, Design, FlowerCounter


def bouquet_to_string(bouquet: Bouquet) -> str:
    """Returns a string representation of the given Bouquet."""
    flowers = sorted(bouquet.flowers.items())
    flowers_formatted = (f"{count}{flower.species}" for flower, count in flowers)
    return f"{bouquet.name}{bouquet.size}{''.join(flowers_formatted)}"


def design_complexity(design: Design) -> int:
    """Returns an approximation of the design's complexity to create."""
    diversity = 3 * len(design.required)
    abundance = 2 * sum(design.required.values())
    return diversity + abundance + design.additional


def flower_demand(designs: Iterable[Design]) -> FlowerCounter:
    """Returns a dict of flowers and amount required across all designs."""
    elements = (design.required.elements() for design in designs)
    return Counter(chain.from_iterable(elements))


def read_inputs(fp: TextIO) -> Iterator[str]:
    """Yields lines from the given filepointer until an empty line is hit."""
    while line := fp.readline().strip():
        yield line
