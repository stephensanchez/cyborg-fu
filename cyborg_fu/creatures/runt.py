"""Runt - basic wandering enemy creature."""

from __future__ import annotations

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Runt(Creature):
    """Small green creature that wanders randomly. Low threat, low HP."""

    def __init__(self, spawn: tuple[int, int]) -> None:
        super().__init__(
            nature=Nature.RUNT,
            spawn=spawn,
            speed=(1, 1),
            life=100,
            graphic="runt.png",
        )
