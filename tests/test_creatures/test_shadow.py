"""Tests for Shadow decoy."""
from __future__ import annotations
import pygame
from cyborg_fu.creatures.shadow import Shadow
from cyborg_fu.enums import Direction, Nature

class TestShadow:
    def test_nature(self) -> None:
        s = Shadow(spawn=(100, 100), shot_group=pygame.sprite.Group(), facing=Direction.LEFT, running=[0, 0])
        assert s.nature is Nature.ASSASSIN

    def test_life_is_one(self) -> None:
        s = Shadow(spawn=(100, 100), shot_group=pygame.sprite.Group(), facing=Direction.LEFT, running=[0, 0])
        assert s.life == 1
