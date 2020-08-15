from collections import Counter
from io import StringIO
from string import ascii_uppercase

import pytest

from balderdash import generate_designs
from balderdash.types import Bouquet, Flower
from balderdash.utils import (
    design_complexity,
    bouquet_to_string,
    flower_demand,
    read_inputs,
)


@pytest.mark.parametrize("name", ascii_uppercase)
@pytest.mark.parametrize("size", "SL")
def test_bouquet_string(name, size):
    bouquet_flowers = {Flower("a", "S"): 1}
    bouquet = Bouquet(name, size, Counter(bouquet_flowers))
    assert bouquet_to_string(bouquet) == f"{name}{size}1a"


@pytest.mark.parametrize(
    "flowers, expected",
    [
        pytest.param(dict(a=15), "AS15a", id="single flower"),
        pytest.param(dict(a=2, x=12), "AS2a12x", id="multi-flower"),
        pytest.param(dict(x=12, a=2), "AS2a12x", id="reverse-order"),
    ],
)
def test_bouquet_string_flower_specification(flowers, expected):
    bouquet_flowers = {
        Flower(species, "S"): count for species, count in flowers.items()
    }
    bouquet = Bouquet("A", "S", Counter(bouquet_flowers))
    assert bouquet_to_string(bouquet) == expected


@pytest.mark.parametrize(
    "design_strings, expected_name",
    [
        pytest.param(["AL3", "BL15", "CL9"], "ACB", id="additional flower weight"),
        pytest.param(
            ["AL1a1b1c3", "BL3a3", "CL2a1b3"], "BCA", id="design variation weight"
        ),
        pytest.param(
            ["AL1a1b1c7", "BL1a1b4c7", "CL2a2b3c7"], "ABC", id="required flower weight"
        ),
    ],
)
def test_design_complexity_comparison(design_strings, expected_name):
    designs = list(generate_designs(design_strings))
    ordered = sorted(designs, key=design_complexity)
    for design, expected_name in zip(ordered, expected_name):
        assert design.name == expected_name


@pytest.mark.parametrize(
    "design_strings, counts",
    [
        pytest.param(["AL1a2b6"], {"aL": 1, "bL": 2}, id="basic single"),
        pytest.param(
            ["AL1a2b6", "BS2a5x9"],
            {"aL": 1, "bL": 2, "aS": 2, "xS": 5},
            id="non-overlapping",
        ),
        pytest.param(
            ["AL1a2b6", "BS2a5x9", "CL2a2c5", "DS2x2y2z6"],
            {"aL": 3, "bL": 2, "cL": 2, "aS": 2, "xS": 7, "yS": 2, "zS": 2},
            id="overlapping",
        ),
    ],
)
def test_flower_demand(design_strings, counts):
    designs = list(generate_designs(design_strings))
    expected_counts = {Flower(*flower): count for flower, count in counts.items()}
    assert flower_demand(designs) == expected_counts


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param("one\ntwo\n", ["one", "two"], id="newline-separated"),
        pytest.param("one\ntwo", ["one", "two"], id="without trailing"),
        pytest.param("one \n two", ["one", "two"], id="empty line separates block"),
        pytest.param("one\n\nnew-block", ["one"], id="empty line separates block"),
    ],
)
def test_read_inputs(input, expected):
    assert list(read_inputs(StringIO(input))) == expected
