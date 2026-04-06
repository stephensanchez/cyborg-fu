"""Shadow - decoy clone spawned by the Assassin."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Direction, Nature


class Shadow(Creature):
    """Fake assassin copy with 1 HP. Exists to confuse the player."""

    def __init__(
        self,
        spawn: tuple[int, int],
        shot_group: pygame.sprite.Group[pygame.sprite.Sprite],
        facing: Direction,
        running: list[int],
    ) -> None:
        super().__init__(
            nature=Nature.ASSASSIN,
            spawn=spawn,
            speed=(1, 2),
            life=1,
            graphic="assassin.png",
        )
        self.facing = facing
        self.movepos = running
        self.counter: int = 50
        self.shotcounter: int = 50
        self.attack: pygame.sprite.Group[pygame.sprite.Sprite] = shot_group
