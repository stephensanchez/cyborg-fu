from __future__ import annotations
from unittest.mock import MagicMock
from cyborg_fu.enums import Direction
from cyborg_fu.weapons.block import Block

class TestBlock:
    def test_creation(self) -> None:
        b = Block(position=(420, 10))
        assert b.life == 100

    def test_collision_pushes_back(self) -> None:
        b = Block(position=(420, 10))
        sprite = MagicMock()
        sprite.facing = Direction.RIGHT
        b.collision(sprite)
        assert sprite.movepos == [-1, 0]

    def test_collision_pushes_back_left(self) -> None:
        b = Block(position=(420, 10))
        sprite = MagicMock()
        sprite.facing = Direction.LEFT
        b.collision(sprite)
        assert sprite.movepos == [1, 0]
