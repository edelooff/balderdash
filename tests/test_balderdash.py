import sys
from io import StringIO
from subprocess import PIPE, Popen

import pytest

from balderdash import main

DESIGNS_AND_FLOWERS = "AS1b2\nBL1x1\n\nbS\naS\nxL\nxL"
EXPECTED_BOUQUETS = "AS1a1b\nBL1x\nBL1x\n"


def test_main(capsys):
    del sys.argv[1:]  # avoid problems of parsing command line parameters
    sys.stdin = StringIO(DESIGNS_AND_FLOWERS)
    main()
    captured = capsys.readouterr()
    assert captured.out == EXPECTED_BOUQUETS


def test_entrypoint():
    process = Popen("balderdash", stdin=PIPE, stdout=PIPE, text=True)
    out, err = process.communicate(DESIGNS_AND_FLOWERS)
    assert out == EXPECTED_BOUQUETS


@pytest.mark.parametrize(
    "size, expected",
    [
        pytest.param(0, ["AL1a", "AL1a", "AL1a", "AL1a"], id="zero buffering"),
        pytest.param(2, ["BL2a", "BL2a"], id="small buffer"),
        pytest.param(4, ["XL4a"], id="fully buffered"),
    ],
)
def test_entrypoint_buffer(size, expected):
    command = ["balderdash", f"--buffer={size}"]
    process = Popen(command, stdin=PIPE, stdout=PIPE, text=True)
    stream = "\n".join(["AL1a1", "BL2a2", "XL4a4", "", "aL", "aL", "aL", "aL"])
    out, err = process.communicate(stream)
    assert out.strip() == "\n".join(expected)
