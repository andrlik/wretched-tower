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
from textual.widgets import Footer, Header

from wretched_tower.tower import PerilLevel, Tower


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

    def compute_dice_remaining(self) -> int:
        return self.tower.get_dice_left()

    def compute_tower_color(self) -> Color:
        if self.tower.get_peril_level() == PerilLevel.MORTALITY:
            return Color.parse("red")
        elif self.tower.get_peril_level() == PerilLevel.WOUNDED:
            return Color.parse("yellow")
        elif self.tower.get_peril_level() == PerilLevel.DEAD:
            return Color.parse("purple")
        else:
            return Color.parse("green")

    def watch_tower_color(self, color: Color) -> None:
        self.query_one("#color").styles.color = color

    def on_roll_tower(self, tower: Tower) -> None:
        self.dice_remaining = tower.get_dice_left()
