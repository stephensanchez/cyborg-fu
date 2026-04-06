from __future__ import annotations
from cyborg_fu.stages.stage_one import EnemySlot


class TestEnemySlot:
    def test_initial_state(self) -> None:
        slot = EnemySlot(spawn=(100, 50))
        assert slot.alive is False
        assert slot.creature is None

    def test_mark_alive(self) -> None:
        slot = EnemySlot(spawn=(100, 50))
        slot.alive = True
        assert slot.alive is True

    def test_independent_tracking(self) -> None:
        """Bug B2 regression test."""
        slot_a = EnemySlot(spawn=(100, 50))
        slot_c = EnemySlot(spawn=(300, 50))
        slot_a.alive = True
        slot_c.alive = True
        slot_a.alive = False
        assert slot_c.alive is True
        assert slot_a.alive is False
