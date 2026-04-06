"""Tests for text display classes."""
from __future__ import annotations
import pygame
from cyborg_fu.ui.text import DialogText, MenuText

class TestDialogText:
    def test_initial_life(self) -> None:
        t = DialogText("Hello world")
        assert t.life == 300

    def test_disappears_after_lifetime(self) -> None:
        t = DialogText("Hello world")
        group = pygame.sprite.Group(t)
        for _ in range(300):
            t.update()
        assert t not in group

class TestMenuText:
    def test_persists(self) -> None:
        t = MenuText("Menu option", 50, 150)
        group = pygame.sprite.Group(t)
        for _ in range(500):
            t.update()
        assert t in group
