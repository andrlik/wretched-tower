import dataclasses
import random
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.color import Color
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer, Header


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

    def __init__(self, dice_size: int = 6, dice_amount: int = 100) -> None:
        if dice_size < 2:  # noqa: PLR2004
            msg = "Dice must have more than one side!"
            raise ValueError(msg)
        self._dice_size = dice_size
        self.set_dice_left(dice_amount)
        self.possible_values = self._get_possible_die_values()

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
            die_result = random.randint(1, self._dice_size)  # noqa: S311
            results[die_result] += 1
        self.set_dice_left(self._dice_left - results[1])
        self.roll_distributions.append(
            RollDistribution(dice_rolled=dice_to_roll, dice_results=results)
        )
        return RollResult(dice_rolled=dice_to_roll, dice_lost=results[1])


class TowerApp(App):
    """A TUI that manages a tumbling tower mechanic via die rolls."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = "Wretched Tower"

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """Toggles between dark and light mode."""
        self.theme = (  # type: ignore
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


class TowerWidget(Widget):
    """A widget that displays the current tower."""

    tower = Tower()
    dice_remaining = reactive(100)
    tower_color = reactive(Color.parse("green"))

    HEALTHY_LIMIT: ClassVar[int] = 60
    DEADLY_LIMIT: ClassVar[int] = 25

    def compute_dice_remaining(self) -> int:
        return self.tower.get_dice_left()

    def compute_tower_color(self) -> Color:
        if self.dice_remaining < self.DEADLY_LIMIT:
            return Color.parse("red")
        elif self.dice_remaining < self.HEALTHY_LIMIT:
            return Color.parse("yellow")
        else:
            return Color.parse("green")

    def watch_tower_color(self, color: Color) -> None:
        self.query_one("#color").styles.color = color

    def on_roll_tower(self, tower: Tower) -> None:
        self.dice_remaining = tower.get_dice_left()
