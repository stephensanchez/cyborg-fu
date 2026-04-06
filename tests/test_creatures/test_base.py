"""Tests for the base Creature class."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pygame

from cyborg_fu.constants import KNOCKBACK_FORCE, WALL_MARGIN
from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Direction, Nature, State


def make_creature(**kwargs):
    defaults = {
        "nature": Nature.RUNT,
        "spawn": (100, 100),
        "speed": (1, 1),
        "life": 100,
        "graphic": "runt.png",
    }
    defaults.update(kwargs)
    return Creature(**defaults)


class TestCreatureInit:
    def test_initial_facing(self) -> None:
        c = make_creature()
        assert c.facing is Direction.RIGHT

    def test_initial_state(self) -> None:
        c = make_creature()
        assert c.state is State.STILL

    def test_initial_life(self) -> None:
        c = make_creature(life=200)
        assert c.life == 200


class TestMovement:
    def test_moveup(self) -> None:
        c = make_creature(speed=(3, 3))
        c.moveup()
        assert c.state is State.MOVE_UP
        assert c.movepos[1] == -3

    def test_movedown(self) -> None:
        c = make_creature(speed=(3, 3))
        c.movedown()
        assert c.state is State.MOVE_DOWN
        assert c.movepos[1] == 3

    def test_moveleft(self) -> None:
        c = make_creature(speed=(3, 3))
        c.moveleft()
        assert c.state is State.MOVE_LEFT
        assert c.movepos[0] == -3

    def test_moveright(self) -> None:
        c = make_creature(speed=(3, 3))
        c.moveright()
        assert c.state is State.MOVE_RIGHT
        assert c.movepos[0] == 3


class TestKnockback:
    def test_knockback_reverses_direction(self) -> None:
        c = make_creature()
        c.facing = Direction.RIGHT
        c.knockback()
        assert c.movepos[0] == -KNOCKBACK_FORCE


class TestDeath:
    def test_creature_dies_at_zero_life(self) -> None:
        c = make_creature(life=1)
        c.life = 0
        group = pygame.sprite.Group(c)
        c.update()
        assert c not in group
