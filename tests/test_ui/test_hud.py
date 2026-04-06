"""Tests for HUD elements."""
from __future__ import annotations
from unittest.mock import MagicMock
from cyborg_fu.ui.hud import LifeBar, ManaBar, Score

class TestScore:
    def test_initial_score(self) -> None:
        s = Score()
        assert s.score == 0

    def test_add_points(self) -> None:
        s = Score()
        s.add_points(5)
        assert s.score == 5

    def test_add_points_cumulative(self) -> None:
        s = Score()
        s.add_points(3)
        s.add_points(7)
        assert s.score == 10

class TestLifeBar:
    def test_creation(self) -> None:
        char = MagicMock()
        char.life = 300
        bar = LifeBar(char)
        assert bar.max_life == 300

class TestManaBar:
    def test_creation(self) -> None:
        char = MagicMock()
        char.mana = 100
        bar = ManaBar(char)
        assert bar.max_mana == 300
