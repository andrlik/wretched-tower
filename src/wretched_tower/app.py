# app.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from textual.app import App, ComposeResult
from textual.color import Color
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable, Footer, Header, Label

from wretched_tower.tower import PerilLevel, Tower


class TowerStatus(Widget):
    """A widget that displays the current status of the tower."""

    dice_remaining = reactive(100)
    peril_level = reactive(PerilLevel.HEALTHY)
    tower_color = reactive(Color.parse("green"))

    def __init__(self, tower: Tower) -> None:
        super().__init__()
        self.dice_remaining = tower.get_dice_left()
        self.peril_level = tower.get_peril_level()
        self.tower_color = self.get_tower_color_from_peril_level(self.peril_level)

    @staticmethod
    def get_tower_color_from_peril_level(peril_level: PerilLevel) -> Color:
        match peril_level:
            case PerilLevel.MORTALITY:
                return Color.parse("red")
            case PerilLevel.WOUNDED:
                return Color.parse("yellow")
            case PerilLevel.DEAD:
                return Color.parse("purple")
            case PerilLevel.HEALTHY:
                return Color.parse("green")
            case _:
                return Color.parse("green")

    def compose(self) -> ComposeResult:
        yield Label(renderable="[b]Dice Remaining[/b]")
        yield Label(str(self.dice_remaining), id="dice")
        yield DataTable(name="Roll Results")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Rolled", "1", "2", "3", "4", "5", "6")

    def watch_tower_color(self, color: Color) -> None:
        self.styles.color = color

    def watch_dice_remaining(self, dice_remaining: int) -> None:
        # Redraw the tower.
        # self.query_one("#dice").value = str(dice_remaining)
        pass

    def watch_peril_level(self, peril_level: PerilLevel) -> None:
        self.tower_color = self.get_tower_color_from_peril_level(peril_level)


class TowerApp(App):
    """A TUI that manages a tumbling tower mechanic via die rolls."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("r", "roll_tower", "Roll tower dice"),
        ("ctrl+n", "new_tower", "Start new tower"),
    ]
    TITLE = "Wretched Tower"
    # theme = "tokyo-night"
    tower = Tower()

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()
        yield TowerStatus(tower=self.tower)
        yield Footer()

    def action_toggle_dark(self) -> None:
        """Toggles between dark and light mode."""
        self.theme = (  # type: ignore
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_roll_tower(self) -> None:
        """Roll the tower and send the results to the child widgets as needed."""
        if self.tower.get_dice_left() > 0:
            self.tower.roll_tower()
            tower_status_widget = self.query_one(TowerStatus)
            tower_status_widget.dice_remaining = self.tower.get_dice_left()
            tower_status_widget.peril_level = self.tower.get_peril_level()
            last_result = self.tower.roll_distributions[-1]
            tower_status_widget.query_one(DataTable).add_row(
                last_result.dice_rolled,
                last_result.dice_results[1],
                last_result.dice_results[2],
                last_result.dice_results[3],
                last_result.dice_results[4],
                last_result.dice_results[5],
                last_result.dice_results[6],
            )

    def action_new_tower(self) -> None:
        self.tower = Tower()
        tower_status_widget = self.query_one(TowerStatus)
        tower_status_widget.dice_remaining = self.tower.get_dice_left()
        tower_status_widget.peril_level = self.tower.get_peril_level()
        tower_status_widget.query_one(DataTable).clear()
        dice_display = tower_status_widget.query(Label).last()
        if self.tower.get_dice_left() > 0:
            dice_display.update(content=str(self.tower.get_dice_left()))
        else:
            dice_display.update(content="You have died")
