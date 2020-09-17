"""An over-engineered solution to a small problem: Balderdash!"""

from argparse import ArgumentParser, FileType
from collections import Counter
from itertools import islice
from typing import Iterable, Iterator, Optional

from .parser import generate_designs, generate_flowers
from .types import Bouquet, Design, Flower, FlowerCounter
from .utils import bouquet_to_string, design_complexity, flower_demand, read_lines

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
    pool: FlowerCounter = Counter(islice(flowers, buffer))
    try:
        while True:
            if bouquet := bouquet_from_designs(designs, pool, demand):
                under_buffer = max(0, buffer - sum(pool.values()))
                pool.update(islice(flowers, under_buffer))
                yield bouquet
            else:
                pool[next(flowers)] += 1
    except StopIteration:
        return


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
    parser = ArgumentParser()
    parser.add_argument(
        "infile",
        nargs="?",
        default="-",
        type=FileType("r"),
        help="File with design and flower inputs, to use instead of stdin",
    )
    parser.add_argument(
        "--buffer",
        default=250,
        type=int,
        help="Number of flowers to collect before bouquet creation (default: 250)",
    )
    args = parser.parse_args()

    designs = list(generate_designs(read_lines(args.infile)))
    designs.sort(key=design_complexity, reverse=True)
    flowers = generate_flowers(read_lines(args.infile))
    for bouquet in generate_bouquets(flowers, designs, buffer=args.buffer):
        print(bouquet_to_string(bouquet))
