"""ThrownBlade - Tesi's projectile blade attack."""
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.constants import BLADE_RETURN_FRAME, BLADE_STOP_FRAME, BLADE_THROW_SPEED, WALL_MARGIN
from cyborg_fu.enums import Direction, State


class ThrownBlade(pygame.sprite.Sprite):
    """A spinning blade thrown by Tesi that returns after traveling a distance."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = 60
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("blade.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()  # type: ignore[union-attr]
        self.clock: int = 1
        self.state: State = State.STILL
        self.original: pygame.Surface = self.image
        self.movepos: list[int] = [0, 0]
        self._init_direction(facing)

    def _init_direction(self, facing: Direction) -> None:
        """Set initial movement direction for the thrown blade."""
        self.rect.midtop = self.position  # type: ignore[union-attr]
        self.state = State.MOVING
        speed = BLADE_THROW_SPEED
        if facing is Direction.RIGHT:
            self.movepos = [speed, 0]
        elif facing is Direction.LEFT:
            self.movepos = [-speed, 0]
        elif facing is Direction.DOWN:
            self.movepos = [0, speed]
        elif facing is Direction.UP:
            self.movepos = [0, -speed]

    def update(self) -> None:
        """Move and spin the blade each frame."""
        self._on_wall()
        newpos = self.rect.move(self.movepos)  # type: ignore[union-attr]
        if self.state is State.STILL:
            self.movepos = [0, 0]
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
        if self.state is not State.STILL:
            self._spin()

    def _spin(self) -> None:
        """Rotate the blade image and handle return/stop logic."""
        center: tuple[int, int] = self.rect.center  # type: ignore[union-attr,assignment]
        self.clock += 30
        self.image = pygame.transform.rotate(self.original, self.clock)
        self.rect = self.image.get_rect(center=center)
        if BLADE_RETURN_FRAME <= self.clock <= BLADE_RETURN_FRAME + 1:
            self.movepos[0] = -self.movepos[0]
            self.movepos[1] = -self.movepos[1]
        elif self.clock >= BLADE_STOP_FRAME:
            self.state = State.STILL

    def _on_wall(self) -> None:
        """Stop blade movement when it hits a wall boundary."""
        if (self.rect.left < self.area.left + WALL_MARGIN  # type: ignore[union-attr]
                or self.rect.right > self.area.right - WALL_MARGIN  # type: ignore[union-attr]
                or self.rect.top < self.area.top + WALL_MARGIN  # type: ignore[union-attr]
                or self.rect.bottom > self.area.bottom - WALL_MARGIN):  # type: ignore[union-attr]
            self.state = State.STILL
