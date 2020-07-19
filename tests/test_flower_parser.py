from itertools import product, zip_longest
from string import ascii_lowercase

import pytest

from balderdash.parser import generate_flowers
from balderdash.types import Flower


@pytest.mark.parametrize("size", "SL")
@pytest.mark.parametrize("species", ascii_lowercase)
def test_parse_flower(flower_parser, species, size):
    flower = flower_parser(f"{species}{size}")
    assert isinstance(flower, Flower)
    assert flower.species == species
    assert flower.size == size


@pytest.mark.parametrize(
    "pattern",
    [
        pytest.param("AL", id="uppercase species"),
        pytest.param("Al", id="lowercase size"),
        pytest.param("A l", id="whitespace-1"),
        pytest.param("Al ", id="whitespace-2"),
    ],
)
def test_create_flower_bad_syntax(flower_parser, pattern):
    with pytest.raises(ValueError, match="Bad flower syntax"):
        flower_parser(pattern)


def test_generate_flowers():
    patterns = ["".join(flower) for flower in product(ascii_lowercase, "SL")]
    flowers = list(generate_flowers(patterns))
    for flower, (species, size) in zip_longest(flowers, patterns):
        assert isinstance(flower, Flower)
        assert flower.species == species
        assert flower.size == size
