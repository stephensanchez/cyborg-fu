"""Tests for game enums."""

from cyborg_fu.enums import Direction, Nature, State


class TestDirection:
    def test_all_directions_exist(self) -> None:
        assert Direction.UP is not None
        assert Direction.DOWN is not None
        assert Direction.LEFT is not None
        assert Direction.RIGHT is not None

    def test_opposite(self) -> None:
        assert Direction.UP.opposite is Direction.DOWN
        assert Direction.DOWN.opposite is Direction.UP
        assert Direction.LEFT.opposite is Direction.RIGHT
        assert Direction.RIGHT.opposite is Direction.LEFT

    def test_rotation_degrees(self) -> None:
        assert Direction.UP.rotation == 0
        assert Direction.DOWN.rotation == 180
        assert Direction.LEFT.rotation == 90
        assert Direction.RIGHT.rotation == 270


class TestNature:
    def test_hero_natures(self) -> None:
        assert Nature.TESI.is_hero is True
        assert Nature.GUNNER.is_hero is True

    def test_enemy_natures(self) -> None:
        assert Nature.RUNT.is_hero is False
        assert Nature.OGRE.is_hero is False
        assert Nature.ASSASSIN.is_hero is False

    def test_wanderers(self) -> None:
        assert Nature.RUNT.wanders is True
        assert Nature.ASSASSIN.wanders is True
        assert Nature.OGRE.wanders is False
