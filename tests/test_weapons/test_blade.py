from __future__ import annotations
import pygame
from cyborg_fu.enums import Direction
from cyborg_fu.weapons.blade import Blade
from cyborg_fu.weapons.thrown_blade import ThrownBlade

class TestBlade:
    def test_lifetime(self) -> None:
        b = Blade(position=(100, 100), facing=Direction.RIGHT)
        assert b.life == 10

    def test_dies_after_lifetime(self) -> None:
        b = Blade(position=(100, 100), facing=Direction.RIGHT)
        group = pygame.sprite.Group(b)
        for _ in range(10):
            b.update()
        assert b not in group

class TestThrownBlade:
    def test_lifetime(self) -> None:
        tb = ThrownBlade(position=(100, 100), facing=Direction.RIGHT)
        assert tb.life == 60

    def test_moves_right(self) -> None:
        tb = ThrownBlade(position=(100, 100), facing=Direction.RIGHT)
        assert tb.movepos == [6, 0]

    def test_moves_left(self) -> None:
        tb = ThrownBlade(position=(100, 100), facing=Direction.LEFT)
        assert tb.movepos == [-6, 0]

    def test_all_directions(self) -> None:
        for direction, expected in [
            (Direction.RIGHT, [6, 0]),
            (Direction.LEFT, [-6, 0]),
            (Direction.UP, [0, -6]),
            (Direction.DOWN, [0, 6]),
        ]:
            tb = ThrownBlade(position=(100, 100), facing=direction)
            assert tb.movepos == expected
