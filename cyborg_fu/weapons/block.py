"""Block - impassable terrain obstacle."""
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction

if TYPE_CHECKING:
    from cyborg_fu.creatures.base import Creature

class Block(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__()
        self.life: int = 100
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("block.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.rect.midtop = self.position
        pygame.event.pump()

    def collision(self, sprite: "Creature") -> None:
        sprite.movepos = [0, 0]
        if sprite.facing is Direction.LEFT:
            sprite.movepos = [1, 0]
        elif sprite.facing is Direction.RIGHT:
            sprite.movepos = [-1, 0]
        elif sprite.facing is Direction.UP:
            sprite.movepos = [0, 1]
        elif sprite.facing is Direction.DOWN:
            sprite.movepos = [0, -1]
