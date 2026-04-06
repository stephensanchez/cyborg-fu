"""Ogre - heavy enemy that chases and clubs the player."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Ogre(Creature):
    """Big, slow, strong enemy. Chases player and swings a club."""

    def __init__(
        self, spawn: tuple[int, int], club_group: pygame.sprite.Group[pygame.sprite.Sprite]
    ) -> None:
        super().__init__(
            nature=Nature.OGRE,
            spawn=spawn,
            speed=(1, 1),
            life=500,
            graphic="ogre.png",
        )
        self.counter: int = 10
        self.clubcounter: int = 5
        self.attack: pygame.sprite.Group[pygame.sprite.Sprite] = club_group
