"""Blade - Tesi's melee swing attack."""
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction, State

class Blade(pygame.sprite.Sprite):
    """Spinning blade that appears briefly during Tesi's melee attack."""
    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = 10
        self.state: State = State.STILL
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("blade.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.original: pygame.Surface = self.image
        self._init_position(facing)

    def _init_position(self, facing: Direction) -> None:
        self.rect.midtop = self.position
        self.state = State.MOVING
        if facing is Direction.RIGHT:
            self.movepos = [40, 0]
        elif facing is Direction.LEFT:
            self.movepos = [-40, 0]
        elif facing is Direction.DOWN:
            self.image = pygame.transform.rotate(self.image, 90)
            self.movepos = [0, 20]
        elif facing is Direction.UP:
            self.image = pygame.transform.rotate(self.image, 90)
            self.movepos = [0, -70]
        else:
            self.movepos = [0, 0]
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def update(self) -> None:
        self.life -= 1
        if self.life == 0:
            self.kill()
