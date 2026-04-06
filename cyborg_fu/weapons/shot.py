"""Shot - basic bullet projectile."""
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.constants import SHOT_LIFETIME, SHOT_SPEED, WALL_MARGIN
from cyborg_fu.enums import Direction, State


class Shot(pygame.sprite.Sprite):
    """Basic bullet projectile that travels in a straight line."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = SHOT_LIFETIME
        self.state: State = State.STILL
        self.image, self.rect = load_png("bullet.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()  # type: ignore[union-attr]
        self.movepos: list[int] = [0, 0]
        self._init_direction(position, facing)

    def _init_direction(self, position: tuple[int, int], facing: Direction) -> None:
        """Set movement direction based on facing."""
        self.rect.midtop = position  # type: ignore[union-attr]
        if facing is Direction.RIGHT:
            self.movepos = [SHOT_SPEED, 0]
        elif facing is Direction.LEFT:
            self.movepos = [-SHOT_SPEED, 0]
        elif facing is Direction.DOWN:
            self.movepos = [0, SHOT_SPEED]
        elif facing is Direction.UP:
            self.movepos = [0, -SHOT_SPEED]

    def update(self) -> None:
        """Move the shot each frame and kill it if off-screen or expired."""
        self._on_wall()
        self.life -= 1
        newpos = self.rect.move(self.movepos)  # type: ignore[union-attr]
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
        if self.life == 0:
            self.kill()

    def _on_wall(self) -> None:
        """Kill the shot if it hits a wall boundary."""
        if (self.rect.left < self.area.left + WALL_MARGIN  # type: ignore[union-attr]
                or self.rect.right > self.area.right - WALL_MARGIN  # type: ignore[union-attr]
                or self.rect.top < self.area.top + WALL_MARGIN  # type: ignore[union-attr]
                or self.rect.bottom > self.area.bottom - WALL_MARGIN):  # type: ignore[union-attr]
            self.kill()
