"""An over-engineered solution to a small problem: Balderdash!"""

import sys
from collections import Counter
from itertools import islice
from typing import Iterable, Iterator, Optional

from .parser import generate_designs, generate_flowers
from .types import Bouquet, Design, Flower, FlowerCounter
from .utils import bouquet_to_string, design_complexity, flower_demand, read_inputs

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


def main() -> None:
    designs = list(generate_designs(read_inputs(sys.stdin)))
    designs.sort(key=design_complexity, reverse=True)
    flowers = generate_flowers(read_inputs(sys.stdin))
    for bouquet in generate_bouquets(flowers, designs):
        print(bouquet_to_string(bouquet))
