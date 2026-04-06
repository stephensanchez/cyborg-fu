"""Text display sprites for dialog and menus."""

from __future__ import annotations

import pygame

from cyborg_fu.constants import COLOR_BLACK, COLOR_GREEN


class DialogText(pygame.sprite.Sprite):
    """Temporary text that disappears after a set number of frames."""

    def __init__(self, text: str, life: int = 300) -> None:
        super().__init__()
        self.font: pygame.font.Font = pygame.font.Font(None, 20)
        self.text: str = text
        self.life: int = life
        self.image: pygame.Surface = self.font.render(self.text, False, COLOR_BLACK)
        self.rect: pygame.Rect = self.image.get_rect().move(20, 20)

    def update(self) -> None:
        """Decrease life counter, re-render text, and kill when expired."""
        self.life -= 1
        self.image = self.font.render(self.text, False, COLOR_BLACK)
        if self.life <= 0:
            self.kill()


class MenuText(pygame.sprite.Sprite):
    """Persistent text for menu screens (doesn't expire)."""

    def __init__(self, text: str, loc_x: int, loc_y: int) -> None:
        super().__init__()
        self.font: pygame.font.Font = pygame.font.Font(None, 20)
        self.text: str = text
        self.loc_x: int = loc_x
        self.loc_y: int = loc_y
        self.image: pygame.Surface = self.font.render(self.text, False, COLOR_GREEN)
        self.rect: pygame.Rect = self.image.get_rect().move(self.loc_x, self.loc_y)

    def update(self) -> None:
        """Re-render and reposition the menu text each frame."""
        self.image = self.font.render(self.text, False, COLOR_GREEN)
        self.rect = self.image.get_rect().move(self.loc_x, self.loc_y)
