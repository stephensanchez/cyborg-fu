"""HUD elements: score counter, life bar, mana bar."""

from __future__ import annotations

from typing import Protocol

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.constants import DEFAULT_MAX_MANA


class HasLife(Protocol):
    """Protocol for objects with a life attribute."""
    life: int


class HasMana(Protocol):
    """Protocol for objects with a mana attribute."""
    mana: int


class Score(pygame.sprite.Sprite):
    """Displays and tracks the player's score."""

    def __init__(self) -> None:
        super().__init__()
        self.score: int = 0
        self.font: pygame.font.Font = pygame.font.Font(None, 20)
        self._last_score: int = -1
        self.image: pygame.Surface = self.font.render("Score:   0         ", False, (0, 0, 255))
        self.rect: pygame.Rect = self.image.get_rect().move(450, 550)

    def add_points(self, points: int) -> None:
        """Add points to the score (Bug B4: renamed from 'int' parameter)."""
        self.score += points

    def update(self) -> None:
        """Re-render the score text when it changes."""
        if self.score != self._last_score:
            self._last_score = self.score
            msg = f"Score:   {self.score}         "
            self.image = self.font.render(msg, False, (0, 0, 255))


class LifeBar(pygame.sprite.Sprite):
    """Visual health bar that scales with character's life."""

    def __init__(self, char: HasLife) -> None:
        super().__init__()
        self.char: HasLife = char
        self.max_life: int = char.life
        self.image, self.rect = load_png("health.png")
        self.rect = self.image.get_rect().move(50, 550)

    def update(self) -> None:
        """Resize the bar proportional to current life."""
        x_scale = float(self.char.life) / float(self.max_life) * 300
        self.image = pygame.transform.scale(self.image, (max(1, int(x_scale)), 17))


class ManaBar(pygame.sprite.Sprite):
    """Visual mana bar that scales with character's mana."""

    def __init__(self, char: HasMana) -> None:
        super().__init__()
        self.char: HasMana = char
        self.max_mana: int = DEFAULT_MAX_MANA
        self.image, self.rect = load_png("mana.png")
        self.rect = self.image.get_rect().move(50, 570)

    def update(self) -> None:
        """Resize the bar proportional to current mana."""
        x_scale = (float(self.char.mana) / float(self.max_mana) * 300) + 1
        self.image = pygame.transform.scale(self.image, (int(x_scale), 17))
