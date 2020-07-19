from functools import partial

import pytest

from balderdash.parser import get_parser, create_design, create_flower


@pytest.fixture(scope="session")
def design_parser():
    parser = get_parser("design")
    return partial(create_design, parser)


@pytest.fixture(scope="session")
def flower_parser():
    parser = get_parser("flower")
    return partial(create_flower, parser)
