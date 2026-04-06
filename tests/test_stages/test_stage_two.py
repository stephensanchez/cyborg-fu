from __future__ import annotations
from cyborg_fu.stages.stage_two import OgreSlot


class TestOgreSlot:
    def test_initial_state(self) -> None:
        slot = OgreSlot(spawn=(100, 50))
        assert slot.alive is False
        assert slot.creature is None

    def test_independent_tracking(self) -> None:
        slot_a = OgreSlot(spawn=(100, 50))
        slot_b = OgreSlot(spawn=(200, 50))
        slot_a.alive = True
        assert slot_b.alive is False
