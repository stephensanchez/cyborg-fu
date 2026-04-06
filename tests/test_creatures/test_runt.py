"""Tests for Runt enemy."""
from __future__ import annotations
from cyborg_fu.creatures.runt import Runt
from cyborg_fu.enums import Nature

class TestRunt:
    def test_nature(self) -> None:
        r = Runt(spawn=(100, 100))
        assert r.nature is Nature.RUNT

    def test_life(self) -> None:
        r = Runt(spawn=(100, 100))
        assert r.life == 100

    def test_speed(self) -> None:
        r = Runt(spawn=(100, 100))
        assert r.speed == (1, 1)
