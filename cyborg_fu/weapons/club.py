"""Club - Ogre's melee attack weapon."""
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction, State


class Club(pygame.sprite.Sprite):
    """A spinning club weapon used by ogres in melee attacks."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = 10
        self.state: State = State.STILL
        self.clock: int = 0
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("club.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()  # type: ignore[union-attr]
        self.movepos: list[int] = [0, 0]
        self._init_position(facing)

    def _init_position(self, facing: Direction) -> None:
        """Set initial position and orientation based on ogre's facing direction."""
        self.rect.midtop = self.position  # type: ignore[union-attr]
        self.state = State.MOVING
        assert self.image is not None
        if facing is Direction.RIGHT:
            self.movepos = [35, 0]
        elif facing is Direction.LEFT:
            self.image = pygame.transform.rotate(self.image, 180)
            self.movepos = [-40, 0]
        elif facing is Direction.DOWN:
            self.image = pygame.transform.rotate(self.image, 270)
            self.movepos = [0, 30]
        elif facing is Direction.UP:
            self.image = pygame.transform.rotate(self.image, 90)
            self.movepos = [0, -50]
        self.original: pygame.Surface = self.image
        newpos = self.rect.move(self.movepos)  # type: ignore[union-attr]
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def _spin(self) -> None:
        """Rotate the club image to create a spinning effect."""
        center: tuple[int, int] = self.rect.center  # type: ignore[union-attr,assignment]
        self.clock += 5
        self.image = pygame.transform.rotate(self.original, self.clock)
        self.rect = self.image.get_rect(center=center)

    def update(self) -> None:
        """Spin the club and kill it when its lifetime expires."""
        self._spin()
        self.life -= 1
        if self.life == 0:
            self.kill()
