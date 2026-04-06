"""Game enumerations for directions, creature types, and states."""

from __future__ import annotations

from enum import Enum


class Direction(Enum):
    """Cardinal directions for movement and facing."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @property
    def opposite(self) -> Direction:
        """Return the opposite direction (used for knockback)."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]

    @property
    def rotation(self) -> int:
        """Pygame rotation angle for this direction."""
        rotations = {
            Direction.UP: 0,
            Direction.DOWN: 180,
            Direction.LEFT: 90,
            Direction.RIGHT: 270,
        }
        return rotations[self]


class Nature(Enum):
    """Creature type identifiers."""

    TESI = "tesi"
    GUNNER = "gunner"
    RUNT = "runt"
    OGRE = "ogre"
    ASSASSIN = "assassin"
    PROF = "prof"

    @property
    def is_hero(self) -> bool:
        """Whether this creature type is player-controlled."""
        return self in (Nature.TESI, Nature.GUNNER)

    @property
    def wanders(self) -> bool:
        """Whether this creature type randomly wanders."""
        return self in (Nature.RUNT, Nature.ASSASSIN)


class State(Enum):
    """Creature movement/action states."""

    STILL = "still"
    MOVE_UP = "moveup"
    MOVE_DOWN = "movedown"
    MOVE_LEFT = "moveleft"
    MOVE_RIGHT = "moveright"
    MOVING = "moving"
