"""Hero/Gunner - the gun-wielding hero character."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Hero(Creature):
    """Gun-toting hero. Can double-fire and use power shots."""

    def __init__(self, attack_group: pygame.sprite.Group[pygame.sprite.Sprite]) -> None:
        super().__init__(
            nature=Nature.GUNNER,
            spawn=(650, 550),
            speed=(3, 3),
            life=100,
            graphic="hero.png",
        )
        self.attack: pygame.sprite.Group[pygame.sprite.Sprite] = attack_group
        self.mana: int = 0
        self.exp: int = 0
