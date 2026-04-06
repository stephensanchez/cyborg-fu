from __future__ import annotations
from cyborg_fu.stages.stage_three import MIDDLE_BLOCKS, EAST_BLOCKS, WEST_BLOCKS, TAUNT_MESSAGES


class TestStageThreeConstants:
    def test_block_counts(self) -> None:
        assert len(MIDDLE_BLOCKS) == 17
        assert len(EAST_BLOCKS) == 9
        assert len(WEST_BLOCKS) == 9

    def test_taunt_messages_exist(self) -> None:
        assert len(TAUNT_MESSAGES) == 5

    def test_all_block_coords_are_tuples(self) -> None:
        for block in MIDDLE_BLOCKS + EAST_BLOCKS + WEST_BLOCKS:
            assert isinstance(block, tuple)
            assert len(block) == 2
