import pytest

from wretched_tower.tower import Tower


@pytest.mark.parametrize(
    "dice_size,expected_results",
    [
        (6, [1, 2, 3, 4, 5, 6]),
        (10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        (8, [1, 2, 3, 4, 5, 6, 7, 8]),
    ],
)
def test_possible_die_values(dice_size, expected_results) -> None:
    tower = Tower(dice_size=dice_size)
    assert tower.possible_values == expected_results


@pytest.mark.parametrize("dice_size", [-1, 0, 1])
def test_invalid_dice_size(dice_size) -> None:
    with pytest.raises(ValueError):
        Tower(dice_size=dice_size)


@pytest.mark.parametrize("dice_amount", [-2, 104])
def test_invalid_dice_amount(dice_amount) -> None:
    with pytest.raises(ValueError):
        Tower(dice_amount=dice_amount)
