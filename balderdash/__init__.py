import sys
from collections import Counter
from itertools import chain
from typing import Iterable, Iterator, Optional, TextIO

from .parser import generate_designs, generate_flowers
from .types import Bouquet, Design, Flower, FlowerCounter


def flower_demand(designs: Iterable[Design]) -> FlowerCounter:
    """Returns a dict of flowers and amount required across all designs."""
    elements = (design.required.elements() for design in designs)
    return Counter(chain.from_iterable(elements))


def generate_bouquets(
    flowers: Iterable[Flower], designs: Iterable[Design]
) -> Iterator[Bouquet]:
    demand = flower_demand(designs)
    pool: FlowerCounter = Counter()
    for flower in flowers:
        pool[flower] += 1
        for design in (design for design in designs if design.size == flower.size):
            if (bouquet := make_bouquet(design, pool, demand)) is not None:
                yield bouquet


def make_bouquet(
    design: Design, pool: FlowerCounter, demand: FlowerCounter
) -> Optional[Bouquet]:
    for flower, qty in design.required.items():
        if pool[flower] < qty:
            return None
    remainder = pool - design.required
    remainder = Counter(flw for flw in remainder.elements() if flw.size == design.size)
    if sum(remainder.values()) < design.additional:
        return None
    bouquet = Bouquet(design.name, design.size, design.required.copy())
    stress = {flower: demand[flower] / qty for flower, qty in remainder.items()}
    for _ in range(design.additional):
        flower = min(stress, key=stress.get)
        remainder[flower] -= 1
        bouquet.flowers[flower] += 1
        try:
            stress[flower] = demand[flower] / remainder[flower]
        except ZeroDivisionError:
            del remainder[flower], stress[flower]
    pool -= bouquet.flowers
    return bouquet


def bouquet_string(bouquet: Bouquet) -> str:
    """Returns a string representation of the given Bouquet."""
    flowers = sorted(bouquet.flowers.items())
    flowers_formatted = (f"{count}{flower.species}" for flower, count in flowers)
    return f"{bouquet.name}{bouquet.size}{''.join(flowers_formatted)}"


def read_inputs(fp: TextIO) -> Iterator[str]:
    """Yields lines from the given filepointer until an empty line is hit."""
    while line := fp.readline().strip():
        yield line


def main() -> None:
    designs = list(generate_designs(read_inputs(sys.stdin)))
    flower_stream = generate_flowers(read_inputs(sys.stdin))
    for bouquet in generate_bouquets(flower_stream, designs):
        print(bouquet_string(bouquet))
