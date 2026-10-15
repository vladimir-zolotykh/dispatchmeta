import pytest
from compress_dir.compress import merge


@pytest.mark.parametrize(
    "args, expected",
    [
        (([1, 2, 3], [1, 0]), [1, 2, 3, 0]),
        (([1, 2, 3], [4, 0]), [1, 2, 3, [4, 0]]),
        (([], [3, 1]), [[3, 1]]),
        (([], [1, 0]), [0]),
    ],
)
def test_merge(args, expected):
    assert merge(*args) == expected
