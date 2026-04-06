"""Tests for Tesi (sword hero)."""
from __future__ import annotations
import pygame
from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import Nature

class TestTesi:
    def test_nature(self) -> None:
        t = Tesi(pygame.sprite.Group())
        assert t.nature is Nature.TESI

    def test_life(self) -> None:
        t = Tesi(pygame.sprite.Group())
        assert t.life == 300

    def test_has_healing(self) -> None:
        t = Tesi(pygame.sprite.Group())
        assert t.healing == 0

    def test_speed(self) -> None:
        t = Tesi(pygame.sprite.Group())
        assert t.speed == (3, 3)
