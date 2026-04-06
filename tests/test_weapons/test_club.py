from __future__ import annotations
import pygame
from cyborg_fu.enums import Direction
from cyborg_fu.weapons.club import Club

class TestClub:
    def test_lifetime(self) -> None:
        c = Club(position=(100, 100), facing=Direction.RIGHT)
        assert c.life == 10

    def test_dies_after_lifetime(self) -> None:
        c = Club(position=(100, 100), facing=Direction.RIGHT)
        group = pygame.sprite.Group(c)
        for _ in range(10):
            c.update()
        assert c not in group
