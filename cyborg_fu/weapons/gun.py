"""Gun - visual weapon attachment (largely cosmetic)."""
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction, State


class Gun(pygame.sprite.Sprite):
    """Visual gun sprite attached to the Hero character."""

    def __init__(  # pylint: disable=unused-argument
        self, char_position: tuple[int, int], facing: Direction
    ) -> None:
        super().__init__()
        self.state: State = State.STILL
        self.positioning: tuple[int, int] = char_position
        self.image, self.rect = load_png("gun.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()  # type: ignore[union-attr]
        self.movepos: list[int] = [0, 0]
        self.rect.midtop = self.positioning

    def update(self) -> None:
        """Move the gun sprite each frame."""
        newpos = self.rect.move(self.movepos)  # type: ignore[union-attr]
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
