import pytest
from compress_dir.compress import compr


@pytest.mark.parametrize(
    "args, expected",
    [
        (([], [3, 0], []), [[3, 0]]),
        (([], [1, 0], []), [0]),
        (([1, 1, 1], []), [[3, 1]]),
        (([1, 0, 1, 0, 1, 0], []), [1, 0, 1, 0, 1, 0]),
        (([1, 1, 1, 0, 1, 0, 0, 0, 0, 1], []), [[3, 1], 0, 1, [4, 0], 1]),
    ],
)
def test_compr(args, expected):
    assert compr(*args) == expected
