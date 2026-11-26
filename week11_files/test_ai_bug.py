import pytest

from bug3_logic import find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([70, 85, 60, 95], 95),
        ([10, 20, 30], 30),
        ([1, 2], 2),
        ([95, 85, 70, 60], 95),
        ([42], 42),
        ([-8, -2, -10], -2),
        ([3, 9, 9, 1], 9),
    ],
)
def test_최댓값을_정확히_반환한다(scores, expected):
    assert find_max(scores) == expected


def test_빈_리스트이면_IndexError가_발생한다():
    with pytest.raises(IndexError):
        find_max([])
