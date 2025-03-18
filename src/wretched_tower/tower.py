# tower.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import dataclasses
import random
from enum import Enum
from typing import ClassVar


class PerilLevel(Enum):
    HEALTHY = 1
    WOUNDED = 2
    MORTALITY = 3
    DEAD = 4


@dataclasses.dataclass
class RollDistribution:
    dice_rolled: int
    dice_results: dict[int, int]


@dataclasses.dataclass
class RollResult:
    dice_rolled: int
    dice_lost: int


@dataclasses.dataclass
class Tower:
    """
    A given instance of the dice tower.

    Attributes:
        roll_distributions (list[dict[int,int]]): A list of the previous roll results
            and their counts.
        possible_values (list[int]): A list of the possible die values based on size.
    """

    roll_distributions: list[RollDistribution]
    possible_values: list[int]
    _dice_size: int = 6
    _dice_left: int = 100

    HEALTHY_LIMIT: ClassVar[int] = 60
    FATAL_LIMIT: ClassVar[int] = 25

    def __init__(self, dice_size: int = 6, dice_amount: int = 100) -> None:
        if dice_size < 2:  # noqa: PLR2004
            msg = "Dice must have more than one side!"
            raise ValueError(msg)
        self._dice_size = dice_size
        self.set_dice_left(dice_amount)
        self.possible_values = self._get_possible_die_values()
        self.roll_distributions = []

    def __str__(self) -> str:  # no cov
        return f"Tower ({self.get_dice_left()}"

    def get_dice_left(self) -> int:  # no cov
        return self._dice_left

    def set_dice_left(self, dice_left: int) -> None:
        if dice_left > 100:  # noqa: PLR2004
            msg = "Tower cannot exceed 100 dice!"
            raise ValueError(msg)
        elif dice_left < 0:
            msg = "Tower dice amount cannot be a negative number!"
            raise ValueError(msg)
        self._dice_left = dice_left

    def _get_possible_die_values(self) -> list[int]:
        """Get a list of all the possible values based on the dice size."""
        current_value = 1
        possible_values = []
        while current_value <= self._dice_size:
            possible_values.append(current_value)
            current_value += 1
        return possible_values

    def get_result_dict_template(self) -> dict[int, int]:
        """Get a dictionary of possible dice values and zeroed counts."""
        results = {}
        for x in self.possible_values:
            results[x] = 0
        return results

    def roll_tower(self) -> RollResult:
        """
        Using the dice remaining, roll them and then remove any that are ones,
        recording the results.
        """
        dice_to_roll = self.get_dice_left()
        results = self.get_result_dict_template()
        for x in self.possible_values:
            results[x] = 0
        for _x in range(self._dice_left):
            die_result = random.randint(1, self._dice_size)  # nosec  # noqa: S311
            results[die_result] += 1
        self.set_dice_left(self._dice_left - results[1])
        self.roll_distributions.append(
            RollDistribution(dice_rolled=dice_to_roll, dice_results=results)
        )
        return RollResult(dice_rolled=dice_to_roll, dice_lost=results[1])

    def get_peril_level(self) -> PerilLevel:
        if self._dice_left == 0:
            return PerilLevel.DEAD
        elif self._dice_left < self.FATAL_LIMIT:
            return PerilLevel.MORTALITY
        elif self._dice_left < self.HEALTHY_LIMIT:
            return PerilLevel.WOUNDED
        else:
            return PerilLevel.HEALTHY
