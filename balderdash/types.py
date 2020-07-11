from typing import Counter, NamedTuple

FlowerCounter = Counter["Flower"]


class Bouquet(NamedTuple):
    name: str
    size: str
    flowers: FlowerCounter


class Design(NamedTuple):
    name: str
    size: str
    required: FlowerCounter
    additional: int


class Flower(NamedTuple):
    species: str
    size: str
