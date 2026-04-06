"""Tests for Hero/Gunner."""
from __future__ import annotations
import pygame
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.enums import Nature

class TestHero:
    def test_nature(self) -> None:
        h = Hero(pygame.sprite.Group())
        assert h.nature is Nature.GUNNER

    def test_life(self) -> None:
        h = Hero(pygame.sprite.Group())
        assert h.life == 100

    def test_speed(self) -> None:
        h = Hero(pygame.sprite.Group())
        assert h.speed == (3, 3)
