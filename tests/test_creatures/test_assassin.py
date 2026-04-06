"""Tests for Assassin boss."""
from __future__ import annotations
import pygame
from cyborg_fu.creatures.assassin import Assassin
from cyborg_fu.enums import Nature

class TestAssassin:
    def test_nature(self) -> None:
        a = Assassin(spawn=(100, 100), shot_group=pygame.sprite.Group())
        assert a.nature is Nature.ASSASSIN

    def test_life(self) -> None:
        a = Assassin(spawn=(100, 100), shot_group=pygame.sprite.Group())
        assert a.life == 400

    def test_has_shot_counter(self) -> None:
        a = Assassin(spawn=(100, 100), shot_group=pygame.sprite.Group())
        assert a.shotcounter == 10
