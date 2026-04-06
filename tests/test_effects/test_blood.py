from __future__ import annotations
import pygame
from cyborg_fu.effects.blood import Blood

class TestBlood:
    def test_lifetime(self) -> None:
        b = Blood(position=(100, 100))
        assert b.life == 100

    def test_dies_after_lifetime(self) -> None:
        b = Blood(position=(100, 100))
        group = pygame.sprite.Group(b)
        for _ in range(100):
            b.update()
        assert b not in group

    def test_has_movement_direction(self) -> None:
        b = Blood(position=(200, 200))
        assert hasattr(b, "movepos")
        assert isinstance(b.movepos, list)
        assert len(b.movepos) == 2
