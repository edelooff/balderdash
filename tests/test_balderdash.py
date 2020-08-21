import sys
from io import StringIO
from subprocess import PIPE, Popen

from balderdash import main

DESIGNS_AND_FLOWERS = "AS1b2\nBL1x1\n\nbS\naS\nxL\nxL"
EXPECTED_BOUQUETS = "AS1a1b\nBL1x\nBL1x\n"


def test_main(capsys):
    sys.stdin = StringIO(DESIGNS_AND_FLOWERS)
    main()
    captured = capsys.readouterr()
    assert captured.out == EXPECTED_BOUQUETS


def test_entrypoint():
    process = Popen('balderdash', stdin=PIPE, stdout=PIPE, text=True)
    out, err = process.communicate(DESIGNS_AND_FLOWERS)
    assert out == EXPECTED_BOUQUETS
