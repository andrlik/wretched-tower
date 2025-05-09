# Wretched Tower

A digital dice-based tool to use as an alternative to tumbling tower mechanics used in games, such as those based on the [Wretched and Alone SRD](https://sealedlibrary.itch.io/wretched-alone-srd) by Sealed Library.

[![PyPI -- Version](https://img.shields.io/pypi/v/wretched-tower)](https://pypi.org/project/wretched-tower/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/andrlik/wretched-tower/blob/main/.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/andrlik/wretched-tower)](https://github.com/andrlik/wretched-tower/blob/main/LICENSE)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/andrlik/wretched-tower/releases)
![Test results](https://github.com/andrlik/wretched-tower/actions/workflows/ci.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/andrlik/wretched-tower/badge.svg?branch=main)](https://coveralls.io/github/andrlik/wretched-tower?branch=main)

## The mechanic

The idea for the mechanic was [originally posted](https://itch.io/jam/wretched-jam/topic/796498/dice-substitute-for-jenga-towers) by user Speak the Sky during a game jam for the SRD.

> Obviously a Jenga tower is a bit more specialised than dice or cards, and can't really been done easily and properly online, so here's a simple mechanic that uses d6s (and an online dice roller like orokos.com):
>
> 1. 1st pull: roll 100(!)d6, take out the 1s,
> 2. 2nd pull: roll the dice you have left, take out the 1s etc.
> 3. 'lose' when you run out of dice.
>
> 100d6 is a lot, which is why you should do this digitally!

## The app

The application is implemented as a TUI which you can access via the command line. It creates a tower,
handles dice rolls on demand, and provides feedback on how close to utter destruction you happen to be.

![Screenshot of the Wretched tower app showing dice remaining and key bindings at the bottom. Currently displays 100 dice and healthy.](imgs/Wretched_Tower_2025-03-21T16_24_56_232995.svg)

## Installation

You can install wretched-tower like any other Python application via pip, but you can also sidestep needing to maintain an environment for it by using [uv](https://docs.astral.sh/uv/).

```
uvx wretched-tower
```

## Usage

Simply press ++r++ to roll the tower and the display will update.

![Screenshot of the Wretched Tower app in progress, this time showing 47 dice remaining and status Wounded](imgs/Wretched_Tower_2025-03-21T16_29_08_450953.svg)

If you want to start a new tower, press ++ctrl++ + ++n++.
