"""Blood - splatter effect when a creature takes damage."""
from __future__ import annotations
import random
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.constants import BLOOD_LIFETIME, BLOOD_SPEED

class Blood(pygame.sprite.Sprite):
    """Blood splatter effect spawned when a creature takes damage."""

    DIRECTIONS: list[list[int]] = [
        [BLOOD_SPEED, 0], [0, BLOOD_SPEED], [BLOOD_SPEED, BLOOD_SPEED],
        [-BLOOD_SPEED, -BLOOD_SPEED], [-BLOOD_SPEED, 0], [0, -BLOOD_SPEED],
        [BLOOD_SPEED, -BLOOD_SPEED], [-BLOOD_SPEED, BLOOD_SPEED],
    ]

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__()
        self.life: int = BLOOD_LIFETIME
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("red.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()  # type: ignore[union-attr]
        self.rect.midtop = self.position
        self.movepos: list[int] = random.choice(self.DIRECTIONS).copy()
        # Bug B3 fix: actually apply the movement
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def update(self) -> None:
        """Decrease life counter and kill the sprite when it expires."""
        self.life -= 1
        if self.life == 0:
            self.kill()
