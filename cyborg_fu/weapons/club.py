"""Club - Ogre's melee attack weapon."""
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction, State

class Club(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = 10
        self.state: State = State.STILL
        self.clock: int = 0
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("club.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.movepos: list[int] = [0, 0]
        self._init_position(facing)

    def _init_position(self, facing: Direction) -> None:
        self.rect.midtop = self.position
        self.state = State.MOVING
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
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def _spin(self) -> None:
        center = self.rect.center
        self.clock += 5
        self.image = pygame.transform.rotate(self.original, self.clock)
        self.rect = self.image.get_rect(center=center)

    def update(self) -> None:
        self._spin()
        self.life -= 1
        if self.life == 0:
            self.kill()
