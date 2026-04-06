"""PowerShot - enhanced bullet with more damage."""
from __future__ import annotations
from cyborg_fu.assets import load_png
from cyborg_fu.constants import POWERSHOT_LIFETIME
from cyborg_fu.enums import Direction
from cyborg_fu.weapons.shot import Shot


class PowerShot(Shot):
    """Enhanced bullet that deals more damage than a standard shot."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__(position, facing)
        self.life = POWERSHOT_LIFETIME
        self.image, self.rect = load_png("powershot.png")
        self._init_direction(position, facing)
