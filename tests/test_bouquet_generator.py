from itertools import zip_longest

from balderdash import generate_bouquets
from balderdash.parser import generate_designs, generate_flowers

import pytest


@pytest.fixture
def designs():
    """Return a list of designs, ordered by complexity."""
    designs = "AL1a1b4", "BL2a2", "CL1a2", "XL1", "YS1"
    return list(generate_designs(designs))


@pytest.mark.parametrize(
    "flowers, expected_names",
    [
        pytest.param(["aL"], "X", id="single large"),
        pytest.param(["aS"], "Y", id="single small"),
        pytest.param(["aL", "bL"], "C", id="single small"),
        pytest.param(["aL", "aL"], "B", id="single small"),
        pytest.param(["aL", "bL", "aL", "bL"], "A", id="most complex"),
        pytest.param(["aL", "aL", "bL"], "BX", id="intiial and spare"),
        pytest.param(["aL", "bL", "bL"], "CX", id="intiial and spare"),
    ],
)
def test_basic_creation(designs, flowers, expected_names):
    flowers = generate_flowers(flowers)
    bouquets = generate_bouquets(flowers, designs)
    for bouquet, expected_name in zip_longest(bouquets, expected_names):
        assert bouquet.name == expected_name


@pytest.mark.parametrize(
    "flowers, buffer_size, expected_names",
    [
        pytest.param(["aL", "aL", "bL"], 10, "BX", id="buffered"),
        pytest.param(["aL", "aL", "bL"], 0, "XXX", id="unbuffered"),
    ],
)
def test_buffering_in_creation(designs, flowers, buffer_size, expected_names):
    flowers = generate_flowers(flowers)
    bouquets = generate_bouquets(flowers, designs, buffer=buffer_size)
    for bouquet, expected_name in zip_longest(bouquets, expected_names):
        assert bouquet.name == expected_name


@pytest.mark.parametrize(
    "buffer_size, expected_names",
    [
        pytest.param(0, "AAAAAAAAAA", id="unbuffered"),
        pytest.param(2, "BBBBB", id="small buffer"),
        pytest.param(3, "BBBBB", id="buffer too small for C+ designs"),
        pytest.param(4, "CCB", id="no refill above threshold"),
    ],
)
def test_buffer_refilling(buffer_size, expected_names):
    designs = list(generate_designs(["DL5", "CL4", "BL2", "AL1"]))
    flowers = generate_flowers(["aL"] * 10)
    bouquets = generate_bouquets(flowers, designs, buffer=buffer_size)
    for bouquet, expected_name in zip_longest(bouquets, expected_names):
        assert bouquet.name == expected_name


@pytest.mark.parametrize(
    "buffer_size, expected_names",
    [
        pytest.param(1, "CC", id="unbuffered"),
        pytest.param(3, "CC", id="assert buffer-growth of 1"),
        pytest.param(10, "DD", id="fully buffered"),
    ],
)
def test_buffer_growth(buffer_size, expected_names):
    designs = list(generate_designs(["DL5", "CL4"]))
    flowers = generate_flowers(["aL"] * 10)
    bouquets = generate_bouquets(flowers, designs, buffer=buffer_size)
    for bouquet, expected_name in zip_longest(bouquets, expected_names):
        assert bouquet.name == expected_name


def test_create_from_buffer_remainder():
    designs = list(generate_designs(["AL3", "BL1"]))
    flowers = generate_flowers(["aL"] * 5)
    bouquets = generate_bouquets(flowers, designs, buffer=100)
    for bouquet, expected_name in zip_longest(bouquets, "ABB"):
        assert bouquet.name == expected_name
