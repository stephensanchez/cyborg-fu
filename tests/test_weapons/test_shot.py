from __future__ import annotations
from cyborg_fu.enums import Direction
from cyborg_fu.weapons.shot import Shot
from cyborg_fu.weapons.power_shot import PowerShot

class TestShot:
    def test_lifetime(self) -> None:
        s = Shot(position=(100, 100), facing=Direction.RIGHT)
        assert s.life == 60

    def test_speed_right(self) -> None:
        s = Shot(position=(100, 100), facing=Direction.RIGHT)
        assert s.movepos == [9, 0]

    def test_speed_up(self) -> None:
        s = Shot(position=(100, 100), facing=Direction.UP)
        assert s.movepos == [0, -9]

class TestPowerShot:
    def test_lifetime(self) -> None:
        ps = PowerShot(position=(100, 100), facing=Direction.RIGHT)
        assert ps.life == 65

    def test_all_directions(self) -> None:
        for direction in Direction:
            ps = PowerShot(position=(100, 100), facing=direction)
            assert ps.movepos != [0, 0]
