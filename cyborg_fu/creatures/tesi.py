"""Tesi - the sword-wielding hero character."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Tesi(Creature):
    """Double-bladed swordsman hero. Can swing, throw blades, and heal."""

    def __init__(self, attack_group: pygame.sprite.Group) -> None:
        super().__init__(
            nature=Nature.TESI,
            spawn=(650, 550),
            speed=(3, 3),
            life=300,
            graphic="tesi.png",
        )
        self.attack: pygame.sprite.Group = attack_group
        self.mana: int = 0
        self.healing: int = 0
        self.exp: int = 0
