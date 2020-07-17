from functools import partial
from itertools import zip_longest
from string import ascii_uppercase

import pytest

from balderdash.parser import (
    get_parser,
    create_design,
    generate_designs,
)
from balderdash.types import Design


@pytest.fixture
def design_parser():
    parser = get_parser("design")
    return partial(create_design, parser)


@pytest.mark.parametrize("name", ascii_uppercase)
@pytest.mark.parametrize("size", "SL")
@pytest.mark.parametrize("flower_count", [5, 12])
def test_create_design_basics(design_parser, name, size, flower_count):
    design = design_parser(f"{name}{size}{flower_count}")
    assert isinstance(design, Design)
    assert design.name == name
    assert design.size == size
    assert design.additional == flower_count


@pytest.mark.parametrize(
    "pattern, name, size, required, additional",
    [
        pytest.param("AL1a5", "A", "L", dict(a=1), 4, id="AL1a5"),
        pytest.param("LL2a2b2c6", "L", "L", dict(a=2, b=2, c=2), 0, id="LL2a2b2c6"),
        pytest.param("LL2a2b2c6", "L", "L", dict(a=2, b=2, c=2), 0, id="LL2a2b2c6"),
    ],
)
def test_create_design_with_required(
    design_parser, pattern, name, size, required, additional
):
    design = design_parser(pattern)
    assert isinstance(design, Design)
    assert design.name == name
    assert design.size == size
    for flower, count in design.required.items():
        assert flower.size == design.size
        assert required[flower.species] == count
    assert design.additional == additional


@pytest.mark.parametrize(
    "pattern",
    [
        pytest.param("aL5", id="lowercase name"),
        pytest.param("Al5", id="lowercase size"),
        pytest.param("AX5", id="illegal size indicator"),
        pytest.param("ALx5", id="missing flower count"),
        pytest.param("AL 2a5", id="whitespace in design"),
        pytest.param("AL-2a5", id="negative flower count"),
        pytest.param("AL-5", id="negative total count"),
    ],
)
def test_create_design_bad_syntax(design_parser, pattern):
    with pytest.raises(ValueError, match="Bad design syntax"):
        design_parser(pattern)


def test_create_design_bad_total_quantity(design_parser):
    with pytest.raises(ValueError, match="required flowers greater than total size"):
        design_parser("AL2a2b3")


def test_create_design_redefined_required_flower(design_parser):
    with pytest.raises(ValueError, match="Multiple definitions"):
        design_parser("AL2a2a5")


def test_create_design_required_flowers_not_alphabetized(design_parser):
    with pytest.raises(ValueError, match="Required flowers not in alphabetical order"):
        design_parser("AL2b2a5")


def test_generate_designs():
    patterns = ["AL1a5", "BS2x2y5"]
    designs = list(generate_designs(patterns))
    for design, pattern in zip_longest(designs, patterns):
        assert isinstance(design, Design)
        assert design.name == pattern[0]
