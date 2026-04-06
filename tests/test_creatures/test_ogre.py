"""Tests for Ogre enemy."""
from __future__ import annotations
import pygame
from cyborg_fu.creatures.ogre import Ogre
from cyborg_fu.enums import Nature

class TestOgre:
    def test_nature(self) -> None:
        o = Ogre(spawn=(100, 100), club_group=pygame.sprite.Group())
        assert o.nature is Nature.OGRE

    def test_life(self) -> None:
        o = Ogre(spawn=(100, 100), club_group=pygame.sprite.Group())
        assert o.life == 500

    def test_has_club_counter(self) -> None:
        o = Ogre(spawn=(100, 100), club_group=pygame.sprite.Group())
        assert o.clubcounter == 5
