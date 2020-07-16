"""An over-engineered solution to a small problem: Balderdash!"""

import sys
from collections import Counter
from itertools import chain, islice
from typing import Iterable, Iterator, Optional, TextIO

from .parser import generate_designs, generate_flowers
from .types import Bouquet, Design, Flower, FlowerCounter

__version__ = "0"  # Forever at nil


def bouquet_from_designs(
    designs: Iterable[Design], pool: FlowerCounter, demand: FlowerCounter
) -> Optional[Bouquet]:
    """Attempts to create a bouquet from each available design in turn."""
    for design in designs:
        if all(pool[flower] >= qty for flower, qty in design.required.items()):
            unused = (pool - design.required).elements()
            remainder = [flower for flower in unused if flower.size == design.size]
            if len(remainder) >= design.additional:
                filler = select_filler(Counter(remainder), demand)
                flowers = design.required + Counter(islice(filler, design.additional))
                pool -= flowers
                return Bouquet(design.name, design.size, flowers)
    return None


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


def generate_bouquets(
    flowers: Iterator[Flower], designs: Iterable[Design], buffer: int = 250
) -> Iterator[Bouquet]:
    demand = flower_demand(designs)
    pool: FlowerCounter = Counter()
    while bundle := list(islice(flowers, buffer)):
        pool.update(bundle)
        if bouquet := bouquet_from_designs(designs, pool, demand):
            yield bouquet
            buffer = sum(bouquet.flowers.values())
    while bouquet := bouquet_from_designs(designs, pool, demand):
        yield bouquet


def select_filler(pool: FlowerCounter, demand: FlowerCounter) -> Iterator[Flower]:
    """Yields Flower least in demand relative to its availability."""
    scarcity = {flower: demand[flower] / pool[flower] for flower in pool}
    while True:
        yield (flower := min(scarcity, key=scarcity.get))
        pool[flower] -= 1
        try:
            scarcity[flower] = demand[flower] / pool[flower]
        except ZeroDivisionError:
            del pool[flower], scarcity[flower]


def read_inputs(fp: TextIO) -> Iterator[str]:
    """Yields lines from the given filepointer until an empty line is hit."""
    while line := fp.readline().strip():
        yield line


def main() -> None:
    designs = list(generate_designs(read_inputs(sys.stdin)))
    designs.sort(key=design_complexity, reverse=True)
    flowers = generate_flowers(read_inputs(sys.stdin))
    for bouquet in generate_bouquets(flowers, designs):
        print(bouquet_to_string(bouquet))
