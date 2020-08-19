import sys
from io import StringIO

from balderdash import main


def test_main(capsys):
    sys.stdin = StringIO("AS1b2\nBL1x1\n\nbS\naS\nxL\nxL")
    main()
    captured = capsys.readouterr()
    assert captured.out == "AS1a1b\nBL1x\nBL1x\n"
