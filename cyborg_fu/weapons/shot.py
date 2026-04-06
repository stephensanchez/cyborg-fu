"""Shot - basic bullet projectile."""
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.constants import SHOT_LIFETIME, SHOT_SPEED, WALL_MARGIN
from cyborg_fu.enums import Direction, State

class Shot(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = SHOT_LIFETIME
        self.state: State = State.STILL
        self.image, self.rect = load_png("bullet.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.movepos: list[int] = [0, 0]
        self._init_direction(position, facing)

    def _init_direction(self, position: tuple[int, int], facing: Direction) -> None:
        self.rect.midtop = position
        if facing is Direction.RIGHT:
            self.movepos = [SHOT_SPEED, 0]
        elif facing is Direction.LEFT:
            self.movepos = [-SHOT_SPEED, 0]
        elif facing is Direction.DOWN:
            self.movepos = [0, SHOT_SPEED]
        elif facing is Direction.UP:
            self.movepos = [0, -SHOT_SPEED]

    def update(self) -> None:
        self._on_wall()
        self.life -= 1
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
        if self.life == 0:
            self.kill()

    def _on_wall(self) -> None:
        if (self.rect.left < self.area.left + WALL_MARGIN
            or self.rect.right > self.area.right - WALL_MARGIN
            or self.rect.top < self.area.top + WALL_MARGIN
            or self.rect.bottom > self.area.bottom - WALL_MARGIN):
            self.kill()
