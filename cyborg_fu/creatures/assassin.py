"""Assassin - the final boss enemy."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Assassin(Creature):
    """Tough boss that shoots at the player and spawns shadow decoys."""

    def __init__(self, spawn: tuple[int, int], shot_group: pygame.sprite.Group) -> None:
        super().__init__(
            nature=Nature.ASSASSIN,
            spawn=spawn,
            speed=(1, 1),
            life=400,
            graphic="assassin.png",
        )
        self.counter: int = 50
        self.shotcounter: int = 10
        self.attack: pygame.sprite.Group = shot_group
