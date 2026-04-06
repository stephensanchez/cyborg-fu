"""Entry point for Cyborg-Fu game.

Run with: python -m cyborg_fu
"""

from __future__ import annotations

import sys

from cyborg_fu.stages.stage_one import stage_one
from cyborg_fu.ui.menu import mainmenu


def main() -> None:
    """Launch the game: show menu, then start stages."""
    hero = mainmenu()
    if hero is None:
        sys.exit(0)
    stage_one(hero)


if __name__ == "__main__":
    main()
