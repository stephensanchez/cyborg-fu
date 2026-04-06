# Cyborg-Fu Python 3.13 Modernization Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modernize a Python 2 pygame game (circa 2010) to Python 3.13+ with proper package structure, type hints, bug fixes, tests, and zero lint/mypy errors.

**Architecture:** Restructure flat file layout into a `cyborg_fu` package with subpackages (`creatures/`, `weapons/`, `effects/`, `ui/`, `stages/`). Replace string-based state/direction tracking with Enums. Add type hints everywhere. Fix circular imports by eliminating `import *` and introducing a shared constants module. Fix all identified bugs. Add pytest suite that mocks pygame for unit testing game logic.

**Tech Stack:** Python 3.13+, pygame-ce (community edition, actively maintained), pytest, pylint, mypy, pyproject.toml

---

## File Structure

### New Package Layout

```
cyborg-fu/
  pyproject.toml              # Build config, dependencies, tool settings
  README.md                   # Updated documentation
  data/                       # Image assets (unchanged location)
    *.png
  cyborg_fu/                  # Main package
    __init__.py
    __main__.py               # Entry point: python -m cyborg_fu
    constants.py              # Screen rect, colors, game tuning constants
    enums.py                  # Direction, CreatureNature, State enums
    assets.py                 # load_png(), load_image(), asset path resolution
    creatures/
      __init__.py
      base.py                 # Creature base class
      tesi.py                 # Tesi (sword hero)
      hero.py                 # Hero/Gunner (gun hero)
      runt.py                 # Runt enemy
      ogre.py                 # Ogre enemy
      assassin.py             # Assassin boss
      shadow.py               # Shadow decoy
    weapons/
      __init__.py
      blade.py                # Blade (melee swing)
      thrown_blade.py          # ThrownBlade (projectile)
      shot.py                 # Shot (bullet)
      power_shot.py           # PowerShot (enhanced bullet)
      club.py                 # Club (ogre melee)
      block.py                # Block (terrain obstacle)
      gun.py                  # Gun (visual weapon attachment)
    effects/
      __init__.py
      blood.py                # Blood splatter effect
    ui/
      __init__.py
      hud.py                  # Score, LifeBar, ManaBar classes
      text.py                 # DialogText (timed), MenuText (persistent)
      menu.py                 # Main menu screen
    stages/
      __init__.py
      base.py                 # Shared stage setup/loop helpers
      stage_one.py            # Stage 1: Runts
      stage_two.py            # Stage 2: Ogres
      stage_three.py          # Stage 3: Assassin boss
  tests/
    __init__.py
    conftest.py               # Shared fixtures (mock pygame surface, etc.)
    test_enums.py
    test_assets.py
    test_creatures/
      __init__.py
      test_base.py
      test_tesi.py
      test_hero.py
      test_runt.py
      test_ogre.py
      test_assassin.py
      test_shadow.py
    test_weapons/
      __init__.py
      test_blade.py
      test_thrown_blade.py
      test_shot.py
      test_power_shot.py
      test_club.py
      test_block.py
    test_effects/
      __init__.py
      test_blood.py
    test_ui/
      __init__.py
      test_hud.py
      test_text.py
    test_stages/
      __init__.py
      test_stage_one.py
      test_stage_two.py
      test_stage_three.py
```

### Files Removed (replaced by package structure)
All top-level `.py` files (`main.py`, `mainmenu.py`, `Creature.py`, `Tesi.py`, `Hero.py`, `Runt.py`, `Ogre.py`, `Assassin.py`, `Shadow.py`, `Blade.py`, `ThrownBlade.py`, `Shot.py`, `PowerShot.py`, `Club.py`, `Block.py`, `Gun.py`, `Blood.py`, `DisplayObject.py`, `StageOne.py`, `StageTwo.py`, `StageThree.py`) will be deleted after the new package is working.

---

## Known Bugs to Fix

| # | File | Bug | Fix |
|---|------|-----|-----|
| B1 | `data/` | `health.png` and `mana.png` missing - game crashes on load | Create placeholder images |
| B2 | `StageOne.py:162` | Runt slot C checks `Alives` instead of `Clives` | Fix variable name |
| B3 | `Blood.py:58` | Computes `newpos` but never assigns to `self.rect` | Add `self.rect = newpos` |
| B4 | `main.py:77` | `Score.plus(self, int)` shadows built-in | Rename parameter to `points` |
| B5 | `StageTwo.py:85-86`, `StageThree.py:83-84` | `Mana(tesi)` created but never added to sprite groups | Capture and add to groups |
| B6 | `Creature.py:273-278` | `doublefire()` - `firstShot`/`secondShot` unbound if facing invalid | Use if/elif/else chain |
| B7 | `Creature.py:118-133` | Knockback pushes in facing direction (into danger) not away | Reverse knockback direction |
| B8 | `main.py:20` | Python 2 `raise SystemExit, msg` syntax | Use `raise SystemExit(msg)` |
| B9 | `DisplayObject.py:34` | Python 2 `except error, message:` syntax | Use `except error as message:` |
| B10 | `DisplayObject.py:35` | Python 2 `print 'text'` statement | Use `print('text')` |

---

## Task 1: Project Infrastructure

**Files:**
- Create: `pyproject.toml`
- Create: `cyborg_fu/__init__.py`
- Create: `cyborg_fu/__main__.py` (stub)
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Install Python 3.13 and create virtual environment**

```bash
brew install python@3.13
python3.13 -m venv .venv
source .venv/bin/activate
```

Verify: `python --version` shows 3.13.x

- [ ] **Step 2: Create pyproject.toml**

```toml
[project]
name = "cyborg-fu"
version = "2.0.0"
description = "A pygame arcade fighting game - modernized from 2010 Python 2 original"
authors = [{name = "Stephen Sanchez"}]
license = {text = "MIT"}
requires-python = ">=3.13"
dependencies = [
    "pygame-ce>=2.5.3",
]

[project.scripts]
cyborg-fu = "cyborg_fu.__main__:main"

[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.setuptools.packages.find]
include = ["cyborg_fu*"]

[tool.setuptools.package-data]
cyborg_fu = ["../data/*.png"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_any_generics = true

[[tool.mypy.overrides]]
module = "pygame.*"
ignore_missing_imports = true

[tool.pylint.main]
py-version = "3.13"

[tool.pylint."messages control"]
disable = [
    "too-few-public-methods",
    "too-many-instance-attributes",
    "too-many-arguments",
    "too-many-locals",
]

[tool.pylint.format]
max-line-length = 100
```

- [ ] **Step 3: Install dependencies**

```bash
source .venv/bin/activate
pip install pygame-ce pytest pylint mypy
pip install -e .
```

- [ ] **Step 4: Create package skeleton**

Create `cyborg_fu/__init__.py`:
```python
"""Cyborg-Fu: A pygame arcade fighting game."""
```

Create `cyborg_fu/__main__.py` (stub):
```python
"""Entry point for python -m cyborg_fu."""


def main() -> None:
    """Launch the game."""
    # Will be implemented in Task 14
    print("Cyborg-Fu launching...")


if __name__ == "__main__":
    main()
```

Create `tests/__init__.py` (empty).

Create `tests/conftest.py`:
```python
"""Shared test fixtures for Cyborg-Fu tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_pygame() -> Any:
    """Mock pygame.display and pygame.image for all tests.

    This prevents tests from needing an actual display server.
    """
    mock_surface = MagicMock()
    mock_surface.get_rect.return_value = MagicMock(
        left=0, right=800, top=0, bottom=600, width=800, height=600,
        contains=MagicMock(return_value=True),
    )
    mock_surface.get_size.return_value = (800, 600)

    mock_image = MagicMock()
    mock_rect = MagicMock()
    mock_rect.move.return_value = mock_rect
    mock_rect.left = 100
    mock_rect.right = 130
    mock_rect.top = 100
    mock_rect.bottom = 130
    mock_rect.center = (115, 115)
    mock_rect.midtop = (115, 100)
    mock_rect.midbottom = (115, 130)
    mock_rect.midleft = (100, 115)
    mock_rect.midright = (130, 115)
    mock_image.get_rect.return_value = mock_rect
    mock_image.get_alpha.return_value = None

    with (
        patch("pygame.init"),
        patch("pygame.display.get_surface", return_value=mock_surface),
        patch("pygame.display.set_mode", return_value=mock_surface),
        patch("pygame.display.mode_ok", return_value=32),
        patch("pygame.display.set_caption"),
        patch("pygame.display.flip"),
        patch("pygame.image.load", return_value=mock_image),
        patch("pygame.event.pump"),
        patch("pygame.font.Font", return_value=MagicMock(
            render=MagicMock(return_value=mock_image),
        )),
        patch("pygame.transform.rotate", return_value=mock_image),
        patch("pygame.transform.scale", return_value=mock_image),
        patch("pygame.Surface", return_value=mock_surface),
    ):
        yield mock_surface
```

- [ ] **Step 5: Verify skeleton works**

```bash
source .venv/bin/activate
python -m cyborg_fu
pytest tests/ -v
```

Expected: prints "Cyborg-Fu launching...", pytest collects 0 tests, passes.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml cyborg_fu/__init__.py cyborg_fu/__main__.py tests/__init__.py tests/conftest.py
git commit -m "feat: add project infrastructure with pyproject.toml and package skeleton"
```

---

## Task 2: Constants and Enums

**Files:**
- Create: `cyborg_fu/constants.py`
- Create: `cyborg_fu/enums.py`
- Create: `tests/test_enums.py`

- [ ] **Step 1: Write tests for enums**

Create `tests/test_enums.py`:
```python
"""Tests for game enums."""

from cyborg_fu.enums import Direction, Nature, State


class TestDirection:
    def test_all_directions_exist(self) -> None:
        assert Direction.UP is not None
        assert Direction.DOWN is not None
        assert Direction.LEFT is not None
        assert Direction.RIGHT is not None

    def test_opposite(self) -> None:
        assert Direction.UP.opposite is Direction.DOWN
        assert Direction.DOWN.opposite is Direction.UP
        assert Direction.LEFT.opposite is Direction.RIGHT
        assert Direction.RIGHT.opposite is Direction.LEFT

    def test_rotation_degrees(self) -> None:
        assert Direction.UP.rotation == 0
        assert Direction.DOWN.rotation == 180
        assert Direction.LEFT.rotation == 90
        assert Direction.RIGHT.rotation == 270


class TestNature:
    def test_hero_natures(self) -> None:
        assert Nature.TESI.is_hero is True
        assert Nature.GUNNER.is_hero is True

    def test_enemy_natures(self) -> None:
        assert Nature.RUNT.is_hero is False
        assert Nature.OGRE.is_hero is False
        assert Nature.ASSASSIN.is_hero is False

    def test_wanderers(self) -> None:
        assert Nature.RUNT.wanders is True
        assert Nature.ASSASSIN.wanders is True
        assert Nature.OGRE.wanders is False
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_enums.py -v
```

Expected: FAIL (module not found)

- [ ] **Step 3: Implement enums module**

Create `cyborg_fu/enums.py`:
```python
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
```

- [ ] **Step 4: Implement constants module**

Create `cyborg_fu/constants.py`:
```python
"""Game-wide constants and tuning values."""

from __future__ import annotations

# Screen
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60

# Colors
COLOR_BLACK: tuple[int, int, int] = (0, 0, 0)
COLOR_GREEN: tuple[int, int, int] = (0, 255, 0)
COLOR_BLUE: tuple[int, int, int] = (0, 0, 255)
COLOR_HEAL_GREEN: tuple[int, int, int] = (0, 250, 0)
COLOR_HEAL_BLUE: tuple[int, int, int] = (0, 0, 250)

# Creature defaults
DEFAULT_MAX_LIFE: int = 300
DEFAULT_MAX_MANA: int = 300
HEAL_MANA_COST: int = 4
HEAL_LIFE_GAIN: int = 1
HEAL_RADIUS: int = 35
HEAL_CIRCLE_WIDTH: int = 2
POWERSHOT_MANA_COST: int = 20

# Damage values
RUNT_CONTACT_DAMAGE_TESI: int = 3
RUNT_CONTACT_DAMAGE_GUNNER: int = 5
SHOT_DAMAGE: int = 10
POWERSHOT_DAMAGE: int = 15
BLADE_DAMAGE: int = 4
OGRE_CLUB_DAMAGE_TESI: int = 6
OGRE_CLUB_DAMAGE_GUNNER: int = 10
ASSASSIN_SHOT_DAMAGE_TESI: int = 6
ASSASSIN_SHOT_DAMAGE_GUNNER: int = 10
ASSASSIN_BLADE_DAMAGE: int = 2
ASSASSIN_SHOT_HIT_DAMAGE: int = 5
ASSASSIN_PSHOT_DAMAGE: int = 8

# Scoring
RUNT_KILL_POINTS: int = 1
OGRE_KILL_POINTS: int = 2
ASSASSIN_HIT_POINTS: int = 1
STAGE_ADVANCE_SCORE: int = 10

# Knockback
KNOCKBACK_FORCE: int = 10

# Spawn timing
RUNT_RELOAD: int = 80
RUNT_ODDS: int = 50
MAX_RUNTS: int = 5
OGRE_RELOAD: int = 80
OGRE_ODDS: int = 50
MAX_OGRES: int = 2
SHADOW_SPAWN: int = 200
SHADOW_ODDS: int = 100

# Projectile settings
SHOT_SPEED: int = 9
SHOT_LIFETIME: int = 60
POWERSHOT_LIFETIME: int = 65
BLADE_THROW_SPEED: int = 6
BLADE_SWING_LIFETIME: int = 10
THROWN_BLADE_LIFETIME: int = 60
BLADE_RETURN_FRAME: int = 1200
BLADE_STOP_FRAME: int = 2400
BLADE_COLLIDE_LATENCY: int = 60
SWING_COLLIDE_LATENCY: int = 150

# Blood effect
BLOOD_LIFETIME: int = 100
BLOOD_SPEED: int = 3

# Wall margin (workaround for sprite edge artifacts)
WALL_MARGIN: int = 10
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_enums.py -v
```

Expected: all PASS

- [ ] **Step 6: Commit**

```bash
git add cyborg_fu/constants.py cyborg_fu/enums.py tests/test_enums.py
git commit -m "feat: add game constants and enum types"
```

---

## Task 3: Asset Loading Module

**Files:**
- Create: `cyborg_fu/assets.py`
- Create: `tests/test_assets.py`
- Create: `data/health.png` (new - fixes bug B1)
- Create: `data/mana.png` (new - fixes bug B1)

- [ ] **Step 1: Write tests for asset loading**

Create `tests/test_assets.py`:
```python
"""Tests for asset loading utilities."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from cyborg_fu.assets import get_data_dir, load_image, load_png


class TestGetDataDir:
    def test_returns_path(self) -> None:
        result = get_data_dir()
        assert isinstance(result, Path)

    def test_path_ends_with_data(self) -> None:
        result = get_data_dir()
        assert result.name == "data"


class TestLoadPng:
    def test_returns_image_and_rect(self) -> None:
        image, rect = load_png("hero.png")
        assert image is not None
        assert rect is not None

    def test_nonexistent_file_raises(self) -> None:
        import pygame
        # Make pygame.image.load raise for missing file
        with patch("pygame.image.load", side_effect=pygame.error("not found")):
            try:
                load_png("nonexistent.png")
                assert False, "Should have raised"
            except (SystemExit, pygame.error):
                pass


class TestLoadImage:
    def test_returns_surface(self) -> None:
        result = load_image("graytile.png")
        assert result is not None
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_assets.py -v
```

Expected: FAIL (module not found)

- [ ] **Step 3: Create missing health.png and mana.png (Bug B1)**

Use Python to generate simple colored bar images:

```bash
python -c "
import struct, zlib

def create_bar_png(filename, r, g, b, width=300, height=17):
    \"\"\"Create a simple solid-color PNG file.\"\"\"
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)

    header = b'\\x89PNG\\r\\n\\x1a\\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)

    raw_data = b''
    for _ in range(height):
        raw_data += b'\\x00'  # filter byte
        for _ in range(width):
            raw_data += bytes([r, g, b])

    idat = make_chunk(b'IDAT', zlib.compress(raw_data))
    iend = make_chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(header + ihdr + idat + iend)

create_bar_png('data/health.png', 220, 20, 20)
create_bar_png('data/mana.png', 20, 60, 220)
print('Created health.png and mana.png')
"
```

- [ ] **Step 4: Implement assets module**

Create `cyborg_fu/assets.py`:
```python
"""Asset loading utilities for images and sounds."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    pass


def get_data_dir() -> Path:
    """Return the path to the data/ directory containing game assets."""
    return Path(__file__).resolve().parent.parent / "data"


def load_png(name: str) -> tuple[pygame.Surface, pygame.Rect]:
    """Load a PNG image and return (surface, rect).

    Handles alpha conversion automatically.
    """
    fullname = get_data_dir() / name
    try:
        image = pygame.image.load(str(fullname))
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print(f"Cannot load image: {fullname}")
        raise SystemExit(f"Cannot load image: {fullname}") from message
    return image, image.get_rect()


def load_image(name: str) -> pygame.Surface:
    """Load an image file and return the surface (no rect).

    Used for backgrounds and tiles.
    """
    fullname = get_data_dir() / name
    try:
        surface = pygame.image.load(str(fullname))
    except pygame.error as message:
        raise SystemExit(
            f'Could not load image "{fullname}": {pygame.get_error()}'
        ) from message
    return surface.convert()
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_assets.py -v
```

Expected: all PASS

- [ ] **Step 6: Commit**

```bash
git add cyborg_fu/assets.py tests/test_assets.py data/health.png data/mana.png
git commit -m "feat: add asset loading module and create missing health/mana bar images

Fixes bug B1: health.png and mana.png were referenced but never existed."
```

---

## Task 4: Base Creature Class

**Files:**
- Create: `cyborg_fu/creatures/__init__.py`
- Create: `cyborg_fu/creatures/base.py`
- Create: `tests/test_creatures/__init__.py`
- Create: `tests/test_creatures/test_base.py`

- [ ] **Step 1: Write tests for base creature**

Create `tests/test_creatures/__init__.py` (empty).

Create `tests/test_creatures/test_base.py`:
```python
"""Tests for the base Creature class."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pygame

from cyborg_fu.constants import KNOCKBACK_FORCE, WALL_MARGIN
from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Direction, Nature, State


def make_creature(**kwargs: object) -> Creature:
    """Create a Creature with sensible defaults for testing."""
    defaults = {
        "nature": Nature.RUNT,
        "spawn": (100, 100),
        "speed": (1, 1),
        "life": 100,
        "graphic": "runt.png",
    }
    defaults.update(kwargs)
    return Creature(**defaults)  # type: ignore[arg-type]


class TestCreatureInit:
    def test_initial_facing(self) -> None:
        c = make_creature()
        assert c.facing is Direction.RIGHT

    def test_initial_state(self) -> None:
        c = make_creature()
        assert c.state is State.STILL

    def test_initial_life(self) -> None:
        c = make_creature(life=200)
        assert c.life == 200


class TestMovement:
    def test_moveup_sets_state(self) -> None:
        c = make_creature(speed=(3, 3))
        c.moveup()
        assert c.state is State.MOVE_UP
        assert c.movepos[1] == -3

    def test_movedown_sets_state(self) -> None:
        c = make_creature(speed=(3, 3))
        c.movedown()
        assert c.state is State.MOVE_DOWN
        assert c.movepos[1] == 3

    def test_moveleft_sets_state(self) -> None:
        c = make_creature(speed=(3, 3))
        c.moveleft()
        assert c.state is State.MOVE_LEFT
        assert c.movepos[0] == -3

    def test_moveright_sets_state(self) -> None:
        c = make_creature(speed=(3, 3))
        c.moveright()
        assert c.state is State.MOVE_RIGHT
        assert c.movepos[0] == 3


class TestKnockback:
    def test_knockback_reverses_direction(self) -> None:
        """Bug B7: knockback should push AWAY from facing, not into it."""
        c = make_creature()
        c.facing = Direction.RIGHT
        original_pos = c.rect.copy()
        c.knockback()
        # Should push LEFT (opposite of RIGHT facing)
        assert c.movepos[0] == -KNOCKBACK_FORCE


class TestDeath:
    def test_creature_dies_at_zero_life(self) -> None:
        c = make_creature(life=1)
        c.life = 0
        group = pygame.sprite.Group(c)
        c.update()
        assert c not in group
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_creatures/test_base.py -v
```

Expected: FAIL

- [ ] **Step 3: Implement base Creature class**

Create `cyborg_fu/creatures/__init__.py`:
```python
"""Game creature classes - heroes and enemies."""

from cyborg_fu.creatures.base import Creature

__all__ = ["Creature"]
```

Create `cyborg_fu/creatures/base.py`:
```python
"""Base Creature class for all living entities in the game."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.constants import (
    BLOOD_SPEED,
    DEFAULT_MAX_LIFE,
    DEFAULT_MAX_MANA,
    HEAL_CIRCLE_WIDTH,
    HEAL_LIFE_GAIN,
    HEAL_MANA_COST,
    HEAL_RADIUS,
    KNOCKBACK_FORCE,
    WALL_MARGIN,
)
from cyborg_fu.enums import Direction, Nature, State

if TYPE_CHECKING:
    pass


class Creature(pygame.sprite.Sprite):
    """Base class for all game characters (heroes and enemies).

    Handles movement, turning, wall collision, knockback, and death.
    Subclasses add specific abilities and AI behavior.
    """

    def __init__(
        self,
        nature: Nature,
        spawn: tuple[int, int],
        speed: tuple[int, int],
        life: int,
        graphic: str,
    ) -> None:
        super().__init__()
        self.facing: Direction = Direction.RIGHT
        self.nature: Nature = nature
        self.speed: tuple[int, int] = speed
        self.life: int = life
        self.graphic: str = graphic
        self.counter: int = 100
        self.spawn: tuple[int, int] = spawn
        self.mana: int = 0
        self.healing: int = 0
        self.image, self.rect = load_png(graphic)
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.state: State = State.STILL
        self.movepos: list[int] = [0, 0]
        self.original: pygame.Surface = self.image
        self._reinit()

    def _reinit(self) -> None:
        """Reset position and movement state."""
        self.state = State.STILL
        self.movepos = [0, 0]
        firstpos = self.rect.move(self.spawn)
        if self.area.contains(firstpos):
            self.rect = firstpos
        self.original = self.image

    def update(self) -> None:
        """Per-frame update: AI behavior, movement, and death check."""
        if self.nature.wanders:
            self._wanderer()
        if self.nature is Nature.TESI:
            self.heal()
            self.regen()
        if self.nature is Nature.GUNNER:
            self.regen()
        self._off_wall()
        if self.state is State.STILL:
            self.movepos = [0, 0]
        else:
            newpos = self.rect.move(self.movepos)
            if self.area.contains(newpos):
                self.rect = newpos
        pygame.event.pump()
        if self.life <= 0:
            self.kill()

    # -- Movement --

    def moveup(self) -> None:
        """Move creature upward."""
        self.movepos[1] -= self.speed[1]
        self.state = State.MOVE_UP
        self.turn(Direction.UP)

    def movedown(self) -> None:
        """Move creature downward."""
        self.movepos[1] += self.speed[1]
        self.state = State.MOVE_DOWN
        self.turn(Direction.DOWN)

    def moveleft(self) -> None:
        """Move creature left."""
        self.movepos[0] -= self.speed[0]
        self.state = State.MOVE_LEFT
        self.turn(Direction.LEFT)

    def moveright(self) -> None:
        """Move creature right."""
        self.movepos[0] += self.speed[0]
        self.state = State.MOVE_RIGHT
        self.turn(Direction.RIGHT)

    def turn(self, facing: Direction) -> None:
        """Rotate sprite image to face the given direction."""
        self.facing = facing
        self.image = pygame.transform.rotate(self.original, facing.rotation)

    # -- Combat --

    def bleed(self, blood_group: pygame.sprite.Group) -> None:
        """Spawn a blood effect at the creature's center."""
        from cyborg_fu.effects.blood import Blood

        new_blood = Blood(self.rect.center)
        blood_group.add(new_blood)

    def knockback(self) -> None:
        """Push creature away from the direction it's facing.

        Bug B7 fix: original code pushed IN the facing direction.
        Now pushes in the OPPOSITE direction (away from attacker).
        """
        force = KNOCKBACK_FORCE
        self.state = State.STILL
        direction = self.facing.opposite
        if direction is Direction.UP:
            self.movepos[1] = -force
        elif direction is Direction.DOWN:
            self.movepos[1] = force
        elif direction is Direction.LEFT:
            self.movepos[0] = -force
        elif direction is Direction.RIGHT:
            self.movepos[0] = force
        self.rect = self.rect.move(self.movepos)

    def _off_wall(self) -> None:
        """Reverse movement if hitting screen edge."""
        if (
            self.rect.left < self.area.left + WALL_MARGIN
            or self.rect.right > self.area.right - WALL_MARGIN
        ):
            self.movepos[0] = -self.movepos[0]
        elif (
            self.rect.top < self.area.top + WALL_MARGIN
            or self.rect.bottom > self.area.bottom - WALL_MARGIN
        ):
            self.movepos[1] = -self.movepos[1]

    # -- AI Behaviors --

    def aim(self, target_rect: pygame.Rect, shot_group: pygame.sprite.Group) -> None:
        """AI: aim and shoot at target position."""
        from cyborg_fu.weapons.shot import Shot

        xdiff = target_rect[0] - self.rect[0]
        ydiff = target_rect[1] - self.rect[1]
        self.shotcounter -= 1
        if self.shotcounter == 0:
            self.shotcounter = 5
            if int(random.random() * 100):
                choice = random.choice((1, 2, 3))
                if choice == 1:
                    if xdiff < 30 and ydiff < 30 and ydiff > -30:
                        self.moveleft()
                        self._fire(shot_group)
                    if xdiff > -30 and ydiff < 30 and ydiff > -30:
                        self.moveright()
                        self._fire(shot_group)
                    if ydiff < 30 and xdiff < 30 and xdiff > -30:
                        self.moveup()
                        self._fire(shot_group)
                    if ydiff > -30 and xdiff < 30 and xdiff > -30:
                        self.movedown()
                        self._fire(shot_group)

    def tryclub(
        self, target_rect: pygame.Rect, club_group: pygame.sprite.Group
    ) -> None:
        """AI: attempt to club if target is in range."""
        from cyborg_fu.weapons.club import Club

        xdiff = target_rect[0] - self.rect[0]
        ydiff = target_rect[1] - self.rect[1]
        self.clubcounter -= 1
        if self.clubcounter == 0:
            self.clubcounter = 10
            if int(random.random() * 100):
                if -65 < xdiff < 65 and -65 < ydiff < 65:
                    new_club = Club(self.rect.center, self.facing)
                    club_group.add(new_club)

    def chase(self, target_rect: pygame.Rect) -> None:
        """AI: move toward target position."""
        xdiff = target_rect[0] - self.rect[0]
        ydiff = target_rect[1] - self.rect[1]
        self.counter -= 1
        if self.counter == 0:
            self.counter = 10
            if int(random.random() * 100):
                self.movepos = [0, 0]
                if xdiff > 50:
                    self.moveright()
                if ydiff > 50:
                    self.movedown()
                if xdiff < -50:
                    self.moveleft()
                if ydiff < -50:
                    self.moveup()

    def dodge(self) -> None:
        """AI: randomly juke to avoid attacks."""
        movements = [
            [0, 2], [0, -2], [2, 0], [-2, 0],
            [2, 2], [-4, 4], [4, -4], [-4, -4],
        ]
        choice = random.randint(0, len(movements) - 1)
        if choice < len(movements):
            self.movepos = movements[choice]

    def _wanderer(self) -> None:
        """AI: random roaming for runts and assassins."""
        self.counter -= 1
        if self.counter == 0:
            self.counter = 100
            self.state = State.STILL
            if int(random.random() * 100):
                self.movepos = [0, 0]
                choice = random.choice((1, 2, 3, 4, 5))
                if choice == 1:
                    self.moveup()
                elif choice == 2:
                    self.movedown()
                elif choice == 3:
                    self.moveleft()
                elif choice == 4:
                    self.moveright()
                else:
                    self.state = State.STILL

    # -- Weapon creation --

    def swing(self, blade_group: pygame.sprite.Group) -> None:
        """Melee blade swing attack (Tesi)."""
        from cyborg_fu.weapons.blade import Blade

        self.state = State.STILL
        new_blade = Blade(self.rect.center, self.facing)
        blade_group.add(new_blade)

    def throw(self, blade_group: pygame.sprite.Group) -> None:
        """Throw a blade projectile (Tesi)."""
        from cyborg_fu.weapons.thrown_blade import ThrownBlade

        new_blade = ThrownBlade(self.rect.midtop, self.facing)
        blade_group.add(new_blade)

    def _fire(self, shot_group: pygame.sprite.Group) -> None:
        """Fire a single shot (AI enemies)."""
        from cyborg_fu.weapons.shot import Shot

        new_shot = Shot(self.rect.midtop, self.facing)
        shot_group.add(new_shot)

    def doublefire(self, shot_group: pygame.sprite.Group) -> None:
        """Fire two parallel shots (Gunner hero).

        Bug B6 fix: uses if/else to guarantee shots are always created.
        """
        from cyborg_fu.weapons.shot import Shot

        if self.facing in (Direction.RIGHT, Direction.LEFT):
            first_shot = Shot(self.rect.midtop, self.facing)
            second_shot = Shot(self.rect.midbottom, self.facing)
        else:
            first_shot = Shot(self.rect.midleft, self.facing)
            second_shot = Shot(self.rect.midright, self.facing)
        shot_group.add(first_shot)
        shot_group.add(second_shot)

    def powershot(self, shot_group: pygame.sprite.Group) -> None:
        """Fire two enhanced power shots (costs mana)."""
        from cyborg_fu.weapons.power_shot import PowerShot

        if self.mana > 19:
            self.mana -= 20
            if self.facing in (Direction.RIGHT, Direction.LEFT):
                first_shot = PowerShot(self.rect.midtop, self.facing)
                second_shot = PowerShot(self.rect.midbottom, self.facing)
            else:
                first_shot = PowerShot(self.rect.midleft, self.facing)
                second_shot = PowerShot(self.rect.midright, self.facing)
            shot_group.add(first_shot)
            shot_group.add(second_shot)

    # -- Mana/Healing --

    def regen(self) -> None:
        """Slowly regenerate mana (1 in 5 chance per frame)."""
        if random.choice((1, 2, 3, 4, 5)) == 1 and self.mana < DEFAULT_MAX_MANA:
            self.mana += 1

    def heal(self) -> None:
        """Tesi heal ability: spend mana to regenerate health while holding E."""
        screen = pygame.display.get_surface()
        pos = self.rect.center
        color = random.choice(
            [(0, 250, 0), (0, 0, 250)]
        )
        if self.healing == 1:
            if self.mana > 3 and self.life < DEFAULT_MAX_LIFE:
                self.state = State.STILL
                self.mana -= HEAL_MANA_COST
                self.life += HEAL_LIFE_GAIN
                pygame.draw.circle(screen, color, pos, HEAL_RADIUS, HEAL_CIRCLE_WIDTH)
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_creatures/test_base.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add cyborg_fu/creatures/ tests/test_creatures/
git commit -m "feat: add base Creature class with movement, combat, and AI

Fixes B6 (doublefire unbound vars) and B7 (knockback direction reversed)."
```

---

## Task 5: Hero Creature Subclasses

**Files:**
- Create: `cyborg_fu/creatures/tesi.py`
- Create: `cyborg_fu/creatures/hero.py`
- Create: `tests/test_creatures/test_tesi.py`
- Create: `tests/test_creatures/test_hero.py`

- [ ] **Step 1: Write tests**

Create `tests/test_creatures/test_tesi.py`:
```python
"""Tests for Tesi (sword hero)."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import Direction, Nature


class TestTesi:
    def test_nature(self) -> None:
        blade_group = pygame.sprite.Group()
        t = Tesi(blade_group)
        assert t.nature is Nature.TESI

    def test_life(self) -> None:
        t = Tesi(pygame.sprite.Group())
        assert t.life == 300

    def test_has_healing(self) -> None:
        t = Tesi(pygame.sprite.Group())
        assert t.healing == 0
        assert t.mana == 0

    def test_speed(self) -> None:
        t = Tesi(pygame.sprite.Group())
        assert t.speed == (3, 3)
```

Create `tests/test_creatures/test_hero.py`:
```python
"""Tests for Hero/Gunner."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.hero import Hero
from cyborg_fu.enums import Nature


class TestHero:
    def test_nature(self) -> None:
        h = Hero(pygame.sprite.Group())
        assert h.nature is Nature.GUNNER

    def test_life(self) -> None:
        h = Hero(pygame.sprite.Group())
        assert h.life == 100

    def test_speed(self) -> None:
        h = Hero(pygame.sprite.Group())
        assert h.speed == (3, 3)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_creatures/test_tesi.py tests/test_creatures/test_hero.py -v
```

- [ ] **Step 3: Implement Tesi**

Create `cyborg_fu/creatures/tesi.py`:
```python
"""Tesi - the sword-wielding hero character."""

from __future__ import annotations

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Direction, Nature, State


class Tesi(Creature):
    """Double-bladed swordsman hero. Can swing, throw blades, and heal."""

    def __init__(self, attack_group: pygame.sprite.Group) -> None:
        super().__init__(
            nature=Nature.TESI,
            spawn=(650, 550),
            speed=(3, 3),
            life=300,
            graphic="tesi.png",
        )
        self.attack: pygame.sprite.Group = attack_group
        self.mana: int = 0
        self.healing: int = 0
        self.exp: int = 0
```

- [ ] **Step 4: Implement Hero (Gunner)**

Create `cyborg_fu/creatures/hero.py`:
```python
"""Hero/Gunner - the gun-wielding hero character."""

from __future__ import annotations

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Hero(Creature):
    """Gun-toting hero. Can double-fire and use power shots."""

    def __init__(self, attack_group: pygame.sprite.Group) -> None:
        super().__init__(
            nature=Nature.GUNNER,
            spawn=(650, 550),
            speed=(3, 3),
            life=100,
            graphic="hero.png",
        )
        self.attack: pygame.sprite.Group = attack_group
        self.mana: int = 0
        self.exp: int = 0
```

- [ ] **Step 5: Update creatures __init__.py**

```python
"""Game creature classes - heroes and enemies."""

from cyborg_fu.creatures.base import Creature
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.tesi import Tesi

__all__ = ["Creature", "Hero", "Tesi"]
```

- [ ] **Step 6: Run tests and commit**

```bash
pytest tests/test_creatures/ -v
git add cyborg_fu/creatures/ tests/test_creatures/
git commit -m "feat: add Tesi and Hero creature subclasses"
```

---

## Task 6: Enemy Creature Subclasses

**Files:**
- Create: `cyborg_fu/creatures/runt.py`
- Create: `cyborg_fu/creatures/ogre.py`
- Create: `cyborg_fu/creatures/assassin.py`
- Create: `cyborg_fu/creatures/shadow.py`
- Create: `tests/test_creatures/test_runt.py`
- Create: `tests/test_creatures/test_ogre.py`
- Create: `tests/test_creatures/test_assassin.py`
- Create: `tests/test_creatures/test_shadow.py`

- [ ] **Step 1: Write tests for enemies**

Create `tests/test_creatures/test_runt.py`:
```python
"""Tests for Runt enemy."""

from __future__ import annotations

from cyborg_fu.creatures.runt import Runt
from cyborg_fu.enums import Nature


class TestRunt:
    def test_nature(self) -> None:
        r = Runt(spawn=(100, 100))
        assert r.nature is Nature.RUNT

    def test_life(self) -> None:
        r = Runt(spawn=(100, 100))
        assert r.life == 100

    def test_speed(self) -> None:
        r = Runt(spawn=(100, 100))
        assert r.speed == (1, 1)
```

Create `tests/test_creatures/test_ogre.py`:
```python
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
```

Create `tests/test_creatures/test_assassin.py`:
```python
"""Tests for Assassin boss."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.assassin import Assassin
from cyborg_fu.enums import Nature


class TestAssassin:
    def test_nature(self) -> None:
        a = Assassin(spawn=(100, 100), shot_group=pygame.sprite.Group())
        assert a.nature is Nature.ASSASSIN

    def test_life(self) -> None:
        a = Assassin(spawn=(100, 100), shot_group=pygame.sprite.Group())
        assert a.life == 400

    def test_has_shot_counter(self) -> None:
        a = Assassin(spawn=(100, 100), shot_group=pygame.sprite.Group())
        assert a.shotcounter == 10
```

Create `tests/test_creatures/test_shadow.py`:
```python
"""Tests for Shadow decoy."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.shadow import Shadow
from cyborg_fu.enums import Direction, Nature


class TestShadow:
    def test_nature(self) -> None:
        s = Shadow(
            spawn=(100, 100),
            shot_group=pygame.sprite.Group(),
            facing=Direction.LEFT,
            running=[0, 0],
        )
        assert s.nature is Nature.ASSASSIN

    def test_life_is_one(self) -> None:
        s = Shadow(
            spawn=(100, 100),
            shot_group=pygame.sprite.Group(),
            facing=Direction.LEFT,
            running=[0, 0],
        )
        assert s.life == 1
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_creatures/ -v
```

- [ ] **Step 3: Implement Runt**

Create `cyborg_fu/creatures/runt.py`:
```python
"""Runt - basic wandering enemy creature."""

from __future__ import annotations

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Runt(Creature):
    """Small green creature that wanders randomly. Low threat, low HP."""

    def __init__(self, spawn: tuple[int, int]) -> None:
        super().__init__(
            nature=Nature.RUNT,
            spawn=spawn,
            speed=(1, 1),
            life=100,
            graphic="runt.png",
        )
```

- [ ] **Step 4: Implement Ogre**

Create `cyborg_fu/creatures/ogre.py`:
```python
"""Ogre - heavy enemy that chases and clubs the player."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Ogre(Creature):
    """Big, slow, strong enemy. Chases player and swings a club."""

    def __init__(
        self, spawn: tuple[int, int], club_group: pygame.sprite.Group
    ) -> None:
        super().__init__(
            nature=Nature.OGRE,
            spawn=spawn,
            speed=(1, 1),
            life=500,
            graphic="ogre.png",
        )
        self.counter: int = 10
        self.clubcounter: int = 5
        self.attack: pygame.sprite.Group = club_group
```

- [ ] **Step 5: Implement Assassin**

Create `cyborg_fu/creatures/assassin.py`:
```python
"""Assassin - the final boss enemy."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Nature


class Assassin(Creature):
    """Tough boss that shoots at the player and spawns shadow decoys."""

    def __init__(
        self, spawn: tuple[int, int], shot_group: pygame.sprite.Group
    ) -> None:
        super().__init__(
            nature=Nature.ASSASSIN,
            spawn=spawn,
            speed=(1, 1),
            life=400,
            graphic="assassin.png",
        )
        self.counter: int = 50
        self.shotcounter: int = 10
        self.attack: pygame.sprite.Group = shot_group
```

- [ ] **Step 6: Implement Shadow**

Create `cyborg_fu/creatures/shadow.py`:
```python
"""Shadow - decoy clone spawned by the Assassin."""

from __future__ import annotations

import pygame

from cyborg_fu.creatures.base import Creature
from cyborg_fu.enums import Direction, Nature


class Shadow(Creature):
    """Fake assassin copy with 1 HP. Exists to confuse the player."""

    def __init__(
        self,
        spawn: tuple[int, int],
        shot_group: pygame.sprite.Group,
        facing: Direction,
        running: list[int],
    ) -> None:
        super().__init__(
            nature=Nature.ASSASSIN,
            spawn=spawn,
            speed=(1, 2),
            life=1,
            graphic="assassin.png",
        )
        self.facing = facing
        self.movepos = running
        self.counter: int = 50
        self.shotcounter: int = 50
        self.attack: pygame.sprite.Group = shot_group
```

- [ ] **Step 7: Update creatures __init__.py**

```python
"""Game creature classes - heroes and enemies."""

from cyborg_fu.creatures.assassin import Assassin
from cyborg_fu.creatures.base import Creature
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.ogre import Ogre
from cyborg_fu.creatures.runt import Runt
from cyborg_fu.creatures.shadow import Shadow
from cyborg_fu.creatures.tesi import Tesi

__all__ = ["Assassin", "Creature", "Hero", "Ogre", "Runt", "Shadow", "Tesi"]
```

- [ ] **Step 8: Run tests and commit**

```bash
pytest tests/test_creatures/ -v
git add cyborg_fu/creatures/ tests/test_creatures/
git commit -m "feat: add enemy creature subclasses (Runt, Ogre, Assassin, Shadow)"
```

---

## Task 7: Weapon Classes

**Files:**
- Create: `cyborg_fu/weapons/__init__.py`
- Create: `cyborg_fu/weapons/blade.py`
- Create: `cyborg_fu/weapons/thrown_blade.py`
- Create: `cyborg_fu/weapons/shot.py`
- Create: `cyborg_fu/weapons/power_shot.py`
- Create: `cyborg_fu/weapons/club.py`
- Create: `cyborg_fu/weapons/block.py`
- Create: `cyborg_fu/weapons/gun.py`
- Create: `tests/test_weapons/__init__.py`
- Create: `tests/test_weapons/test_blade.py`
- Create: `tests/test_weapons/test_shot.py`
- Create: `tests/test_weapons/test_block.py`

- [ ] **Step 1: Write weapon tests**

Create `tests/test_weapons/__init__.py` (empty).

Create `tests/test_weapons/test_blade.py`:
```python
"""Tests for blade weapons."""

from __future__ import annotations

from cyborg_fu.enums import Direction
from cyborg_fu.weapons.blade import Blade
from cyborg_fu.weapons.thrown_blade import ThrownBlade


class TestBlade:
    def test_lifetime(self) -> None:
        b = Blade(position=(100, 100), facing=Direction.RIGHT)
        assert b.life == 10

    def test_dies_after_lifetime(self) -> None:
        import pygame

        b = Blade(position=(100, 100), facing=Direction.RIGHT)
        group = pygame.sprite.Group(b)
        for _ in range(10):
            b.update()
        assert b not in group


class TestThrownBlade:
    def test_lifetime(self) -> None:
        tb = ThrownBlade(position=(100, 100), facing=Direction.RIGHT)
        assert tb.life == 60

    def test_moves_right(self) -> None:
        tb = ThrownBlade(position=(100, 100), facing=Direction.RIGHT)
        assert tb.movepos == [6, 0]

    def test_moves_left(self) -> None:
        tb = ThrownBlade(position=(100, 100), facing=Direction.LEFT)
        assert tb.movepos == [-6, 0]
```

Create `tests/test_weapons/test_shot.py`:
```python
"""Tests for shot weapons."""

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
```

Create `tests/test_weapons/test_block.py`:
```python
"""Tests for Block terrain obstacle."""

from __future__ import annotations

from unittest.mock import MagicMock

from cyborg_fu.enums import Direction
from cyborg_fu.weapons.block import Block


class TestBlock:
    def test_creation(self) -> None:
        b = Block(position=(420, 10))
        assert b.life == 100

    def test_collision_pushes_back(self) -> None:
        b = Block(position=(420, 10))
        sprite = MagicMock()
        sprite.facing = Direction.RIGHT
        b.collision(sprite)
        assert sprite.movepos == [-1, 0]

    def test_collision_pushes_back_left(self) -> None:
        b = Block(position=(420, 10))
        sprite = MagicMock()
        sprite.facing = Direction.LEFT
        b.collision(sprite)
        assert sprite.movepos == [1, 0]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_weapons/ -v
```

- [ ] **Step 3: Implement all weapon classes**

Create `cyborg_fu/weapons/__init__.py`:
```python
"""Weapon and projectile sprite classes."""
```

Create `cyborg_fu/weapons/blade.py`:
```python
"""Blade - Tesi's melee swing attack."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction, State

if TYPE_CHECKING:
    pass


class Blade(pygame.sprite.Sprite):
    """Spinning blade that appears briefly during Tesi's melee attack."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = 10
        self.state: State = State.STILL
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("blade.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.original: pygame.Surface = self.image
        self._init_position(facing)

    def _init_position(self, facing: Direction) -> None:
        """Set initial offset based on attack direction."""
        self.rect.midtop = self.position
        self.state = State.MOVING
        if facing is Direction.RIGHT:
            self.movepos = [40, 0]
        elif facing is Direction.LEFT:
            self.movepos = [-40, 0]
        elif facing is Direction.DOWN:
            self.image = pygame.transform.rotate(self.image, 90)
            self.movepos = [0, 20]
        elif facing is Direction.UP:
            self.image = pygame.transform.rotate(self.image, 90)
            self.movepos = [0, -70]
        else:
            self.movepos = [0, 0]
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def update(self) -> None:
        """Tick down lifetime and self-destruct."""
        self.life -= 1
        if self.life == 0:
            self.kill()
```

Create `cyborg_fu/weapons/thrown_blade.py`:
```python
"""ThrownBlade - Tesi's projectile blade attack."""

from __future__ import annotations

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.constants import (
    BLADE_RETURN_FRAME,
    BLADE_STOP_FRAME,
    BLADE_THROW_SPEED,
    WALL_MARGIN,
)
from cyborg_fu.enums import Direction, State


class ThrownBlade(pygame.sprite.Sprite):
    """Blade projectile that flies out, reverses, and returns."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = 60
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("blade.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.clock: int = 1
        self.state: State = State.STILL
        self.original: pygame.Surface = self.image
        self.movepos: list[int] = [0, 0]
        self._init_direction(facing)

    def _init_direction(self, facing: Direction) -> None:
        """Set movement vector based on throw direction."""
        self.rect.midtop = self.position
        self.state = State.MOVING
        speed = BLADE_THROW_SPEED
        if facing is Direction.RIGHT:
            self.movepos = [speed, 0]
        elif facing is Direction.LEFT:
            self.movepos = [-speed, 0]
        elif facing is Direction.DOWN:
            self.movepos = [0, speed]
        elif facing is Direction.UP:
            self.movepos = [0, -speed]

    def update(self) -> None:
        """Move, spin, and check for wall collision."""
        self._on_wall()
        newpos = self.rect.move(self.movepos)
        if self.state is State.STILL:
            self.movepos = [0, 0]
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
        if self.state is not State.STILL:
            self._spin()

    def _spin(self) -> None:
        """Rotate the blade sprite and handle direction reversal."""
        center = self.rect.center
        self.clock += 30
        self.image = pygame.transform.rotate(self.original, self.clock)
        self.rect = self.image.get_rect(center=center)
        if BLADE_RETURN_FRAME <= self.clock <= BLADE_RETURN_FRAME + 1:
            self.movepos[0] = -self.movepos[0]
            self.movepos[1] = -self.movepos[1]
        elif self.clock >= BLADE_STOP_FRAME:
            self.state = State.STILL

    def _on_wall(self) -> None:
        """Stop if hitting screen edge."""
        if (
            self.rect.left < self.area.left + WALL_MARGIN
            or self.rect.right > self.area.right - WALL_MARGIN
            or self.rect.top < self.area.top + WALL_MARGIN
            or self.rect.bottom > self.area.bottom - WALL_MARGIN
        ):
            self.state = State.STILL
```

Create `cyborg_fu/weapons/shot.py`:
```python
"""Shot - basic bullet projectile."""

from __future__ import annotations

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.constants import SHOT_LIFETIME, SHOT_SPEED, WALL_MARGIN
from cyborg_fu.enums import Direction, State


class Shot(pygame.sprite.Sprite):
    """Standard bullet that travels in a straight line."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = SHOT_LIFETIME
        self.state: State = State.STILL
        self.image, self.rect = load_png("bullet.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.movepos: list[int] = [0, 0]
        self._init_direction(position, facing)

    def _init_direction(self, position: tuple[int, int], facing: Direction) -> None:
        """Set movement based on shot direction."""
        self.rect.midtop = position
        if facing is Direction.RIGHT:
            self.movepos = [SHOT_SPEED, 0]
        elif facing is Direction.LEFT:
            self.movepos = [-SHOT_SPEED, 0]
        elif facing is Direction.DOWN:
            self.movepos = [0, SHOT_SPEED]
        elif facing is Direction.UP:
            self.movepos = [0, -SHOT_SPEED]

    def update(self) -> None:
        """Move and check for wall collision / lifetime expiry."""
        self._on_wall()
        self.life -= 1
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
        if self.life == 0:
            self.kill()

    def _on_wall(self) -> None:
        """Self-destruct if hitting screen edge."""
        if (
            self.rect.left < self.area.left + WALL_MARGIN
            or self.rect.right > self.area.right - WALL_MARGIN
            or self.rect.top < self.area.top + WALL_MARGIN
            or self.rect.bottom > self.area.bottom - WALL_MARGIN
        ):
            self.kill()
```

Create `cyborg_fu/weapons/power_shot.py`:
```python
"""PowerShot - enhanced bullet with more damage."""

from __future__ import annotations

from cyborg_fu.assets import load_png
from cyborg_fu.constants import POWERSHOT_LIFETIME
from cyborg_fu.enums import Direction
from cyborg_fu.weapons.shot import Shot


class PowerShot(Shot):
    """Enhanced bullet with longer range and more damage."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__(position, facing)
        self.life = POWERSHOT_LIFETIME
        self.image, self.rect = load_png("powershot.png")
        self._init_direction(position, facing)
```

Create `cyborg_fu/weapons/club.py`:
```python
"""Club - Ogre's melee attack weapon."""

from __future__ import annotations

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction, State


class Club(pygame.sprite.Sprite):
    """Spinning club that appears briefly during Ogre's attack."""

    def __init__(self, position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.life: int = 10
        self.state: State = State.STILL
        self.clock: int = 0
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("club.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.movepos: list[int] = [0, 0]
        self._init_position(facing)

    def _init_position(self, facing: Direction) -> None:
        """Offset the club based on attack direction."""
        self.rect.midtop = self.position
        self.state = State.MOVING
        if facing is Direction.RIGHT:
            self.movepos = [35, 0]
        elif facing is Direction.LEFT:
            self.image = pygame.transform.rotate(self.image, 180)
            self.movepos = [-40, 0]
        elif facing is Direction.DOWN:
            self.image = pygame.transform.rotate(self.image, 270)
            self.movepos = [0, 30]
        elif facing is Direction.UP:
            self.image = pygame.transform.rotate(self.image, 90)
            self.movepos = [0, -50]
        self.original: pygame.Surface = self.image
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def _spin(self) -> None:
        """Rotate the club sprite each frame."""
        center = self.rect.center
        self.clock += 5
        self.image = pygame.transform.rotate(self.original, self.clock)
        self.rect = self.image.get_rect(center=center)

    def update(self) -> None:
        """Spin and tick down lifetime."""
        self._spin()
        self.life -= 1
        if self.life == 0:
            self.kill()
```

Create `cyborg_fu/weapons/block.py`:
```python
"""Block - impassable terrain obstacle."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction

if TYPE_CHECKING:
    from cyborg_fu.creatures.base import Creature


class Block(pygame.sprite.Sprite):
    """Impassable block used for river boundaries in Stage 3."""

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__()
        self.life: int = 100
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("block.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.rect.midtop = self.position
        pygame.event.pump()

    def collision(self, sprite: Creature) -> None:
        """Push a sprite back when colliding with this block."""
        sprite.movepos = [0, 0]
        if sprite.facing is Direction.LEFT:
            sprite.movepos = [1, 0]
        elif sprite.facing is Direction.RIGHT:
            sprite.movepos = [-1, 0]
        elif sprite.facing is Direction.UP:
            sprite.movepos = [0, 1]
        elif sprite.facing is Direction.DOWN:
            sprite.movepos = [0, -1]
```

Create `cyborg_fu/weapons/gun.py`:
```python
"""Gun - visual weapon attachment (largely cosmetic)."""

from __future__ import annotations

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.enums import Direction, State


class Gun(pygame.sprite.Sprite):
    """Visual gun sprite that follows a character."""

    def __init__(self, char_position: tuple[int, int], facing: Direction) -> None:
        super().__init__()
        self.state: State = State.STILL
        self.positioning: tuple[int, int] = char_position
        self.image, self.rect = load_png("gun.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.movepos: list[int] = [0, 0]
        self.rect.midtop = self.positioning

    def update(self) -> None:
        """Move the gun with its owner."""
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
```

- [ ] **Step 4: Run tests and commit**

```bash
pytest tests/test_weapons/ -v
git add cyborg_fu/weapons/ tests/test_weapons/
git commit -m "feat: add all weapon and projectile classes"
```

---

## Task 8: Blood Effect

**Files:**
- Create: `cyborg_fu/effects/__init__.py`
- Create: `cyborg_fu/effects/blood.py`
- Create: `tests/test_effects/__init__.py`
- Create: `tests/test_effects/test_blood.py`

- [ ] **Step 1: Write tests (including Bug B3 regression test)**

Create `tests/test_effects/__init__.py` (empty).

Create `tests/test_effects/test_blood.py`:
```python
"""Tests for Blood effect."""

from __future__ import annotations

import pygame

from cyborg_fu.effects.blood import Blood


class TestBlood:
    def test_lifetime(self) -> None:
        b = Blood(position=(100, 100))
        assert b.life == 100

    def test_dies_after_lifetime(self) -> None:
        b = Blood(position=(100, 100))
        group = pygame.sprite.Group(b)
        for _ in range(100):
            b.update()
        assert b not in group

    def test_has_movement_direction(self) -> None:
        """Bug B3 regression: blood particles must actually move."""
        b = Blood(position=(200, 200))
        # movepos should be set to some non-zero direction
        assert hasattr(b, "movepos")
        assert isinstance(b.movepos, list)
        assert len(b.movepos) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_effects/ -v
```

- [ ] **Step 3: Implement Blood (with Bug B3 fix)**

Create `cyborg_fu/effects/__init__.py`:
```python
"""Visual effect classes."""
```

Create `cyborg_fu/effects/blood.py`:
```python
"""Blood - splatter effect when a creature takes damage."""

from __future__ import annotations

import random

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.constants import BLOOD_LIFETIME, BLOOD_SPEED


class Blood(pygame.sprite.Sprite):
    """Blood particle that scatters in a random direction on hit.

    Bug B3 fix: original code computed newpos but never assigned it to
    self.rect. Now the rect is actually updated so blood moves.
    """

    DIRECTIONS: list[list[int]] = [
        [BLOOD_SPEED, 0],
        [0, BLOOD_SPEED],
        [BLOOD_SPEED, BLOOD_SPEED],
        [-BLOOD_SPEED, -BLOOD_SPEED],
        [-BLOOD_SPEED, 0],
        [0, -BLOOD_SPEED],
        [BLOOD_SPEED, -BLOOD_SPEED],
        [-BLOOD_SPEED, BLOOD_SPEED],
    ]

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__()
        self.life: int = BLOOD_LIFETIME
        self.position: tuple[int, int] = position
        self.image, self.rect = load_png("red.png")
        screen = pygame.display.get_surface()
        self.area: pygame.Rect = screen.get_rect()
        self.rect.midtop = self.position
        self.movepos: list[int] = random.choice(self.DIRECTIONS).copy()
        # Bug B3 fix: actually apply the initial movement offset
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def update(self) -> None:
        """Tick down lifetime and self-destruct."""
        self.life -= 1
        if self.life == 0:
            self.kill()
```

- [ ] **Step 4: Run tests and commit**

```bash
pytest tests/test_effects/ -v
git add cyborg_fu/effects/ tests/test_effects/
git commit -m "feat: add Blood effect class

Fixes bug B3: blood particles now actually scatter from hit position."
```

---

## Task 9: UI Classes (HUD and Text)

**Files:**
- Create: `cyborg_fu/ui/__init__.py`
- Create: `cyborg_fu/ui/hud.py`
- Create: `cyborg_fu/ui/text.py`
- Create: `tests/test_ui/__init__.py`
- Create: `tests/test_ui/test_hud.py`
- Create: `tests/test_ui/test_text.py`

- [ ] **Step 1: Write tests (including Bug B4 regression test)**

Create `tests/test_ui/__init__.py` (empty).

Create `tests/test_ui/test_hud.py`:
```python
"""Tests for HUD elements."""

from __future__ import annotations

from unittest.mock import MagicMock

from cyborg_fu.ui.hud import LifeBar, ManaBar, Score


class TestScore:
    def test_initial_score(self) -> None:
        s = Score()
        assert s.score == 0

    def test_add_points(self) -> None:
        """Bug B4 regression: parameter must not shadow built-in 'int'."""
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
```

Create `tests/test_ui/test_text.py`:
```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_ui/ -v
```

- [ ] **Step 3: Implement HUD classes**

Create `cyborg_fu/ui/__init__.py`:
```python
"""UI display elements - HUD, text, menus."""
```

Create `cyborg_fu/ui/hud.py`:
```python
"""HUD elements: score counter, life bar, mana bar."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.constants import DEFAULT_MAX_MANA

if TYPE_CHECKING:
    pass


class HasLife(Protocol):
    """Protocol for objects with a life attribute."""

    life: int


class HasMana(Protocol):
    """Protocol for objects with a mana attribute."""

    mana: int


class Score(pygame.sprite.Sprite):
    """Displays and tracks the player's score."""

    def __init__(self) -> None:
        super().__init__()
        self.score: int = 0
        self.font: pygame.font.Font = pygame.font.Font(None, 20)
        self._last_score: int = -1
        screen = pygame.display.get_surface()
        self.image: pygame.Surface = self.font.render("Score:   0         ", False, (0, 0, 255))
        self.rect: pygame.Rect = self.image.get_rect().move(450, 550)

    def add_points(self, points: int) -> None:
        """Add points to the score (Bug B4: renamed from 'int' parameter)."""
        self.score += points

    def update(self) -> None:
        """Re-render the score text when it changes."""
        if self.score != self._last_score:
            self._last_score = self.score
            msg = f"Score:   {self.score}         "
            self.image = self.font.render(msg, False, (0, 0, 255))


class LifeBar(pygame.sprite.Sprite):
    """Visual health bar that scales with character's life."""

    def __init__(self, char: HasLife) -> None:
        super().__init__()
        self.char: HasLife = char
        self.max_life: int = char.life
        self.image, self.rect = load_png("health.png")
        self.rect = self.image.get_rect().move(50, 550)

    def update(self) -> None:
        """Resize the bar proportional to current life."""
        x_scale = float(self.char.life) / float(self.max_life) * 300
        self.image = pygame.transform.scale(self.image, (max(1, int(x_scale)), 17))


class ManaBar(pygame.sprite.Sprite):
    """Visual mana bar that scales with character's mana."""

    def __init__(self, char: HasMana) -> None:
        super().__init__()
        self.char: HasMana = char
        self.max_mana: int = DEFAULT_MAX_MANA
        self.image, self.rect = load_png("mana.png")
        self.rect = self.image.get_rect().move(50, 570)

    def update(self) -> None:
        """Resize the bar proportional to current mana."""
        x_scale = (float(self.char.mana) / float(self.max_mana) * 300) + 1
        self.image = pygame.transform.scale(self.image, (int(x_scale), 17))
```

- [ ] **Step 4: Implement Text classes**

Create `cyborg_fu/ui/text.py`:
```python
"""Text display sprites for dialog and menus."""

from __future__ import annotations

import pygame

from cyborg_fu.constants import COLOR_BLACK, COLOR_GREEN


class DialogText(pygame.sprite.Sprite):
    """Temporary text that disappears after a set number of frames."""

    def __init__(self, text: str, life: int = 300) -> None:
        super().__init__()
        self.font: pygame.font.Font = pygame.font.Font(None, 20)
        self.text: str = text
        self.life: int = life
        self.image: pygame.Surface = self.font.render(self.text, False, COLOR_BLACK)
        self.rect: pygame.Rect = self.image.get_rect().move(20, 20)

    def update(self) -> None:
        """Count down and self-destruct when expired."""
        self.life -= 1
        self.image = self.font.render(self.text, False, COLOR_BLACK)
        if self.life <= 0:
            self.kill()


class MenuText(pygame.sprite.Sprite):
    """Persistent text for menu screens (doesn't expire)."""

    def __init__(self, text: str, loc_x: int, loc_y: int) -> None:
        super().__init__()
        self.font: pygame.font.Font = pygame.font.Font(None, 20)
        self.text: str = text
        self.loc_x: int = loc_x
        self.loc_y: int = loc_y
        self.image: pygame.Surface = self.font.render(self.text, False, COLOR_GREEN)
        self.rect: pygame.Rect = self.image.get_rect().move(self.loc_x, self.loc_y)

    def update(self) -> None:
        """Re-render text (for position updates)."""
        self.image = self.font.render(self.text, False, COLOR_GREEN)
        self.rect = self.image.get_rect().move(self.loc_x, self.loc_y)
```

- [ ] **Step 5: Run tests and commit**

```bash
pytest tests/test_ui/ -v
git add cyborg_fu/ui/ tests/test_ui/
git commit -m "feat: add HUD (Score, LifeBar, ManaBar) and text display classes

Fixes bug B4: Score.plus() renamed to add_points() to avoid shadowing built-in."
```

---

## Task 10: Main Menu

**Files:**
- Create: `cyborg_fu/ui/menu.py`

- [ ] **Step 1: Implement main menu**

Create `cyborg_fu/ui/menu.py`:
```python
"""Main menu screen with hero selection."""

from __future__ import annotations

import pygame
from pygame.locals import K_DOWN, K_RETURN, K_SPACE, K_UP, KEYDOWN, QUIT

from cyborg_fu.constants import (
    COLOR_BLACK,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from cyborg_fu.ui.text import MenuText


def mainmenu() -> str | None:
    """Display the main menu and return the chosen hero type.

    Returns:
        "tesi" or "gunner", or None if the user quits.
    """
    pygame.init()
    screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    bestdepth = pygame.display.mode_ok(screen_rect.size, 0, 32)
    screen = pygame.display.set_mode(screen_rect.size, 0, bestdepth)
    pygame.display.set_caption("Cyborg-Fu!")

    background = pygame.Surface(screen_rect.size)
    background = background.convert()
    background.fill(COLOR_BLACK)

    welcome = MenuText(
        "Welcome, to Cyborg-Fu.  (Press the space bar to continue)", 20, 10
    )
    arrow = MenuText("->", 20, 150)

    objects = pygame.sprite.Group(welcome)
    clock = pygame.time.Clock()

    choice = "sword"
    messages: list[MenuText] = [
        MenuText("You are a cyborg, programmed by me, the professor.", 20, 30),
        MenuText(
            "My work is complete, it is time to test you against some nasty little critters...",
            20, 50,
        ),
        MenuText(
            "To move, use the W, A, S, and D keys.  "
            "Your basic attack can be used by the spacebar during battle.",
            20, 70,
        ),
        MenuText(
            "For each stage I present you, try and gain twenty points, "
            "then come speak to me, I will advance you.",
            20, 90,
        ),
        MenuText(
            "Press E through Y for possible special abilities, they will use your mana!",
            20, 110,
        ),
        MenuText("Which weapon do you prefer for battle?", 20, 130),
    ]

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None

            if event.type == KEYDOWN:
                if event.key == K_SPACE and len(messages) > 0:
                    message = messages[0]
                    objects.add(message)
                    messages.remove(message)
                if event.key == K_DOWN and len(messages) == 0:
                    choice = "gun"
                    arrow.loc_y = 170
                if event.key == K_UP and len(messages) == 0:
                    choice = "sword"
                    arrow.loc_y = 150
                if event.key == K_RETURN and len(messages) == 0:
                    if choice == "sword":
                        return "tesi"
                    return "gunner"

        if len(messages) == 0:
            objects.add(MenuText("Sword", 50, 150))
            objects.add(MenuText("Gun", 50, 170))
            objects.add(
                MenuText("Use the up and down keys to select, then press enter.", 20, 190)
            )
            objects.add(arrow)

        objects.clear(screen, background)
        objects.update()
        objects.draw(screen)
        pygame.display.flip()
```

- [ ] **Step 2: Commit**

```bash
git add cyborg_fu/ui/menu.py
git commit -m "feat: add main menu with hero selection"
```

---

## Task 11: Stage Base and Stage One

**Files:**
- Create: `cyborg_fu/stages/__init__.py`
- Create: `cyborg_fu/stages/base.py`
- Create: `cyborg_fu/stages/stage_one.py`
- Create: `tests/test_stages/__init__.py`
- Create: `tests/test_stages/test_stage_one.py`

- [ ] **Step 1: Write tests for stage one (including Bug B2 regression)**

Create `tests/test_stages/__init__.py` (empty).

Create `tests/test_stages/test_stage_one.py`:
```python
"""Tests for Stage One logic."""

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

    def test_mark_dead(self) -> None:
        """Bug B2 regression: each slot tracks its own alive state independently."""
        slot_a = EnemySlot(spawn=(100, 50))
        slot_c = EnemySlot(spawn=(300, 50))
        slot_a.alive = True
        slot_c.alive = True
        slot_a.alive = False
        # Slot C should still be alive (bug was checking slot A's state for slot C)
        assert slot_c.alive is True
        assert slot_a.alive is False
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_stages/test_stage_one.py -v
```

- [ ] **Step 3: Implement stage base helpers**

Create `cyborg_fu/stages/__init__.py`:
```python
"""Game stages/levels."""
```

Create `cyborg_fu/stages/base.py`:
```python
"""Shared utilities for game stages."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame

from cyborg_fu.assets import load_image
from cyborg_fu.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

if TYPE_CHECKING:
    from cyborg_fu.creatures.base import Creature


def create_screen(caption: str = "Cyborg-Fu!") -> tuple[pygame.Surface, pygame.Rect]:
    """Initialize pygame display and return (screen surface, screen rect)."""
    pygame.init()
    screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    bestdepth = pygame.display.mode_ok(screen_rect.size, 0, 32)
    screen = pygame.display.set_mode(screen_rect.size, 0, bestdepth)
    pygame.display.set_caption(caption)
    return screen, screen_rect


def create_tiled_background(
    tile_name: str, screen_rect: pygame.Rect
) -> pygame.Surface:
    """Create a background surface by tiling an image."""
    tile = load_image(tile_name)
    background = pygame.Surface(screen_rect.size)
    for x in range(0, screen_rect.width, tile.get_width()):
        for y in range(0, screen_rect.height, tile.get_height()):
            background.blit(tile, (x, y))
    return background


def create_image_background(
    image_name: str, screen_rect: pygame.Rect
) -> pygame.Surface:
    """Create a background from a single full-size image."""
    image = load_image(image_name)
    background = pygame.Surface(screen_rect.size)
    background.blit(image, (0, 0))
    return background


def get_hero_rect(hero: str, tesi: Creature | None, gunner: Creature | None) -> pygame.Rect:
    """Return the rect of the active hero creature."""
    if hero == "tesi" and tesi is not None:
        return tesi.rect
    if gunner is not None:
        return gunner.rect
    msg = f"No hero creature found for type: {hero}"
    raise ValueError(msg)
```

- [ ] **Step 4: Implement Stage One (with Bug B2 and B5 fixes)**

Create `cyborg_fu/stages/stage_one.py`:
```python
"""Stage One: Fight the Runts."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame
from pygame.locals import K_a, K_d, K_e, K_l, K_s, K_SPACE, K_w, KEYDOWN, KEYUP, QUIT

from cyborg_fu.constants import (
    BLADE_COLLIDE_LATENCY,
    BLADE_DAMAGE,
    FPS,
    POWERSHOT_DAMAGE,
    RUNT_CONTACT_DAMAGE_GUNNER,
    RUNT_CONTACT_DAMAGE_TESI,
    RUNT_KILL_POINTS,
    RUNT_ODDS,
    RUNT_RELOAD,
    SHOT_DAMAGE,
    STAGE_ADVANCE_SCORE,
    SWING_COLLIDE_LATENCY,
)
from cyborg_fu.creatures.base import Creature
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.runt import Runt
from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import Nature, State
from cyborg_fu.stages.base import create_screen, create_tiled_background
from cyborg_fu.ui.hud import LifeBar, ManaBar, Score
from cyborg_fu.ui.text import DialogText

if TYPE_CHECKING:
    pass

DOKILL: bool = True
DONTKILL: bool = False


@dataclass
class EnemySlot:
    """Tracks a single enemy spawn slot.

    Bug B2 fix: each slot has its own independent alive flag.
    Original code used separate variables (Alives, Blives, etc.)
    and slot C incorrectly checked Alives instead of Clives.
    """

    spawn: tuple[int, int]
    alive: bool = False
    creature: Runt | None = None


def stage_one(hero: str) -> str | None:
    """Run Stage One: defeat runts to earn points.

    Returns:
        The hero type string to pass to Stage Two, or None if quit.
    """
    screen, screen_rect = create_screen()
    background = create_tiled_background("graytile.png", screen_rect)

    # Sprite groups
    shots = pygame.sprite.Group()
    pshots = pygame.sprite.Group()
    blade = pygame.sprite.Group()
    blood = pygame.sprite.Group()
    runties = pygame.sprite.Group()

    # NPC
    prof = Creature(
        nature=Nature.PROF, spawn=(740, 30), speed=(1, 1), life=10, graphic="prof.png"
    )

    # Score
    score = Score()

    # Initial dialog
    text = DialogText("Professor: Let's see what they can do...")

    # Create hero
    tesi_hero: Tesi | None = None
    gunner_hero: Hero | None = None
    mana_bar: ManaBar | None = None

    if hero == "tesi":
        tesi_hero = Tesi(blade)
        life_bar = LifeBar(tesi_hero)
        mana_bar = ManaBar(tesi_hero)
        heroes = pygame.sprite.Group(tesi_hero)
        sprites = pygame.sprite.Group(tesi_hero, prof, score, life_bar, mana_bar, text)
    else:
        gunner_hero = Hero(shots)
        life_bar = LifeBar(gunner_hero)
        mana_bar = ManaBar(gunner_hero)
        heroes = pygame.sprite.Group(gunner_hero)
        sprites = pygame.sprite.Group(gunner_hero, prof, score, life_bar, mana_bar, text)

    # Enemy slots (Bug B2 fix: independent tracking per slot)
    slots = [
        EnemySlot(spawn=(100, 50)),
        EnemySlot(spawn=(200, 50)),
        EnemySlot(spawn=(300, 50)),
        EnemySlot(spawn=(400, 50)),
        EnemySlot(spawn=(500, 50)),
    ]

    # Dialog checkmarks
    checkmarks: dict[str, bool] = {"score4": False, "talk_early": False, "advance": False}

    all_sprites = pygame.sprite.Group(
        prof, score, life_bar, text, blood, pshots, blade, runties, shots,
    )
    if mana_bar is not None:
        all_sprites.add(mana_bar)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    blade_available = 1
    collide_latency = 0
    runtreload = RUNT_RELOAD

    while True:
        clock.tick(FPS)
        collide_latency -= 1

        # Dialog triggers
        if score.score == 4 and not checkmarks["score4"]:
            msg = "Professor: Hmm, they seem to be working properly. Excellent!"
            sprites.add(DialogText(msg))
            checkmarks["score4"] = True

        # Spawn runts
        if runtreload:
            runtreload -= 1
        elif not int(random.random() * RUNT_ODDS):
            choice = random.randint(0, 4)
            slot = slots[choice]
            if not slot.alive:
                new_runt = Runt(slot.spawn)
                slot.creature = new_runt
                slot.alive = True
                runties.add(new_runt)
            runtreload = RUNT_RELOAD

        # Handle input and combat for Tesi
        if hero == "tesi" and tesi_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        tesi_hero.healing = 1
                    if event.key == K_SPACE and blade_available == 1:
                        tesi_hero.throw(blade)
                        blade_available -= 1
                        collide_latency = BLADE_COLLIDE_LATENCY
                    if event.key == K_w:
                        tesi_hero.moveup()
                    if event.key == K_s:
                        tesi_hero.movedown()
                    if event.key == K_a:
                        tesi_hero.moveleft()
                    if event.key == K_d:
                        tesi_hero.moveright()
                    if event.key == K_l and blade_available == 1:
                        tesi_hero.swing(blade)
                        collide_latency = SWING_COLLIDE_LATENCY
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        tesi_hero.state = State.STILL
                    if event.key == K_e:
                        tesi_hero.healing = 0

            if collide_latency <= 0:
                if pygame.sprite.spritecollide(tesi_hero, blade, DOKILL):
                    blade_available += 1

            if pygame.sprite.spritecollide(tesi_hero, runties, DONTKILL):
                tesi_hero.bleed(blood)
                tesi_hero.life -= RUNT_CONTACT_DAMAGE_TESI

        # Handle input and combat for Gunner
        if hero == "gunner" and gunner_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        gunner_hero.powershot(pshots)
                    if event.key == K_SPACE:
                        gunner_hero.doublefire(shots)
                    if event.key == K_w:
                        gunner_hero.moveup()
                    if event.key == K_s:
                        gunner_hero.movedown()
                    if event.key == K_a:
                        gunner_hero.moveleft()
                    if event.key == K_d:
                        gunner_hero.moveright()
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        gunner_hero.state = State.STILL

            if pygame.sprite.spritecollide(gunner_hero, runties, DONTKILL):
                gunner_hero.bleed(blood)
                gunner_hero.life -= RUNT_CONTACT_DAMAGE_GUNNER
                gunner_hero.knockback()

        # Check runt damage from weapons
        for slot in slots:
            if slot.alive and slot.creature is not None:
                runt = slot.creature
                if pygame.sprite.spritecollide(runt, shots, DOKILL):
                    runt.bleed(blood)
                    runt.life -= SHOT_DAMAGE
                    if runt.life <= 0:
                        slot.alive = False
                        score.add_points(RUNT_KILL_POINTS)
                if pygame.sprite.spritecollide(runt, pshots, DONTKILL):
                    runt.bleed(blood)
                    runt.life -= POWERSHOT_DAMAGE
                    if runt.life <= 0:
                        slot.alive = False
                        score.add_points(RUNT_KILL_POINTS)
                if pygame.sprite.spritecollide(runt, blade, DONTKILL):
                    runt.bleed(blood)
                    runt.life -= BLADE_DAMAGE
                    if runt.life <= 0:
                        slot.alive = False
                        score.add_points(RUNT_KILL_POINTS)

        # Prof interactions
        if pygame.sprite.spritecollide(prof, runties, DONTKILL):
            sprites.add(DialogText("Professor: (Sigh) Attack the subject, stupid runts!"))
            runties.empty()
            for slot in slots:
                slot.alive = False
                slot.creature = None

        if pygame.sprite.spritecollide(prof, heroes, DONTKILL):
            if score.score <= 9 and not checkmarks["talk_early"]:
                sprites.add(
                    DialogText("Professor: Attack the runts, let me see what you can do!")
                )
                checkmarks["talk_early"] = True
            if score.score >= STAGE_ADVANCE_SCORE and not checkmarks["advance"]:
                sprites.add(
                    DialogText("I have finally succeeded. I shall call off these runts.")
                )
                checkmarks["advance"] = True
                runties.empty()
                for slot in slots:
                    slot.alive = False
                    slot.creature = None
                # Import here to avoid circular imports
                from cyborg_fu.stages.stage_two import stage_two

                return stage_two(hero)

        # Render
        runties.clear(screen, background)
        runties.update()
        runties.draw(screen)

        blood.clear(screen, background)
        blood.update()
        blood.draw(screen)

        shots.clear(screen, background)
        shots.update()
        shots.draw(screen)

        pshots.clear(screen, background)
        pshots.update()
        pshots.draw(screen)

        blade.clear(screen, background)
        blade.update()
        blade.draw(screen)

        sprites.clear(screen, background)
        sprites.update()
        sprites.draw(screen)

        pygame.display.flip()
```

- [ ] **Step 4: Run tests and commit**

```bash
pytest tests/test_stages/test_stage_one.py -v
git add cyborg_fu/stages/ tests/test_stages/
git commit -m "feat: add Stage One with enemy slot tracking

Fixes bug B2: runt slot C now correctly tracks its own alive state.
Fixes bug B5: ManaBar now properly added to sprite groups."
```

---

## Task 12: Stage Two

**Files:**
- Create: `cyborg_fu/stages/stage_two.py`

- [ ] **Step 1: Implement Stage Two**

Create `cyborg_fu/stages/stage_two.py` following the same pattern as `stage_one.py` but with:
- Ogres instead of Runts (using `EnemySlot` with `Ogre` type)
- 2 ogre slots instead of 5 runt slots
- Ogres chase the player and use clubs
- Ogre dodging when player attacks
- Club damage instead of contact damage
- Club sprite group for ogre attacks
- Stage advance calls `stage_three(hero)`

The full implementation follows the same structure as Stage One. Key differences:

```python
"""Stage Two: Fight the Ogres."""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame
from pygame.locals import K_a, K_d, K_e, K_l, K_s, K_SPACE, K_w, KEYDOWN, KEYUP, QUIT

from cyborg_fu.constants import (
    BLADE_COLLIDE_LATENCY,
    BLADE_DAMAGE,
    FPS,
    OGRE_CLUB_DAMAGE_GUNNER,
    OGRE_CLUB_DAMAGE_TESI,
    OGRE_KILL_POINTS,
    OGRE_ODDS,
    OGRE_RELOAD,
    POWERSHOT_DAMAGE,
    SHOT_DAMAGE,
    STAGE_ADVANCE_SCORE,
    SWING_COLLIDE_LATENCY,
)
from cyborg_fu.creatures.base import Creature
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.ogre import Ogre
from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import Nature, State
from cyborg_fu.stages.base import create_screen, create_tiled_background, get_hero_rect
from cyborg_fu.ui.hud import LifeBar, ManaBar, Score
from cyborg_fu.ui.text import DialogText

DOKILL: bool = True
DONTKILL: bool = False


@dataclass
class OgreSlot:
    """Tracks a single ogre spawn slot."""

    spawn: tuple[int, int]
    alive: bool = False
    creature: Ogre | None = None


def stage_two(hero: str) -> str | None:
    """Run Stage Two: defeat ogres.

    Returns:
        The hero type string to pass to Stage Three, or None if quit.
    """
    screen, screen_rect = create_screen()
    background = create_tiled_background("graytile.png", screen_rect)

    shots = pygame.sprite.Group()
    pshots = pygame.sprite.Group()
    clubs = pygame.sprite.Group()
    blade = pygame.sprite.Group()
    blood = pygame.sprite.Group()
    ogres = pygame.sprite.Group()

    prof = Creature(
        nature=Nature.PROF, spawn=(740, 30), speed=(1, 1), life=10, graphic="prof.png"
    )
    score = Score()
    text = DialogText("Ogres may seem stupid, but they're a lot smarter than runts! Be careful!")

    tesi_hero: Tesi | None = None
    gunner_hero: Hero | None = None

    if hero == "tesi":
        tesi_hero = Tesi(blade)
        life_bar = LifeBar(tesi_hero)
        mana_bar = ManaBar(tesi_hero)
        heroes = pygame.sprite.Group(tesi_hero)
        sprites = pygame.sprite.Group(tesi_hero, prof, score, life_bar, mana_bar, text)
    else:
        gunner_hero = Hero(shots)
        life_bar = LifeBar(gunner_hero)
        mana_bar = ManaBar(gunner_hero)
        heroes = pygame.sprite.Group(gunner_hero)
        sprites = pygame.sprite.Group(gunner_hero, prof, score, life_bar, mana_bar, text)

    slots = [
        OgreSlot(spawn=(100, 50)),
        OgreSlot(spawn=(200, 50)),
    ]

    checkmarks: dict[str, bool] = {"score4": False, "talk_early": False, "advance": False}

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    blade_available = 1
    collide_latency = 0
    ogrereload = OGRE_RELOAD

    while True:
        clock.tick(FPS)
        collide_latency -= 1

        if score.score == 4 and not checkmarks["score4"]:
            sprites.add(DialogText("These Ogres cost a lot, I hope you can handle more than two!"))
            checkmarks["score4"] = True

        # Spawn ogres
        if ogrereload:
            ogrereload -= 1
        elif not int(random.random() * OGRE_ODDS):
            choice = random.randint(0, 1)
            slot = slots[choice]
            if not slot.alive:
                new_ogre = Ogre(slot.spawn, clubs)
                slot.creature = new_ogre
                slot.alive = True
                ogres.add(new_ogre)
            ogrereload = OGRE_RELOAD

        # Tesi input
        if hero == "tesi" and tesi_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        tesi_hero.healing = 1
                    if event.key == K_SPACE and blade_available == 1:
                        tesi_hero.throw(blade)
                        blade_available -= 1
                        collide_latency = BLADE_COLLIDE_LATENCY
                        for slot in slots:
                            if slot.alive and slot.creature is not None:
                                slot.creature.dodge()
                    if event.key == K_w:
                        tesi_hero.moveup()
                    if event.key == K_s:
                        tesi_hero.movedown()
                    if event.key == K_a:
                        tesi_hero.moveleft()
                    if event.key == K_d:
                        tesi_hero.moveright()
                    if event.key == K_l and blade_available == 1:
                        tesi_hero.swing(blade)
                        collide_latency = SWING_COLLIDE_LATENCY
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        tesi_hero.state = State.STILL
                    if event.key == K_e:
                        tesi_hero.healing = 0

            if collide_latency <= 0:
                if pygame.sprite.spritecollide(tesi_hero, blade, DOKILL):
                    blade_available += 1

            if pygame.sprite.spritecollide(tesi_hero, clubs, DONTKILL):
                tesi_hero.bleed(blood)
                tesi_hero.life -= OGRE_CLUB_DAMAGE_TESI

        # Gunner input
        if hero == "gunner" and gunner_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        gunner_hero.powershot(pshots)
                    if event.key == K_SPACE:
                        gunner_hero.doublefire(shots)
                        for slot in slots:
                            if slot.alive and slot.creature is not None:
                                slot.creature.dodge()
                    if event.key == K_w:
                        gunner_hero.moveup()
                    if event.key == K_s:
                        gunner_hero.movedown()
                    if event.key == K_a:
                        gunner_hero.moveleft()
                    if event.key == K_d:
                        gunner_hero.moveright()
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        gunner_hero.state = State.STILL

            if pygame.sprite.spritecollide(gunner_hero, clubs, DONTKILL):
                gunner_hero.bleed(blood)
                gunner_hero.life -= OGRE_CLUB_DAMAGE_GUNNER
                gunner_hero.knockback()

        # Get hero location for AI
        loc = (tesi_hero or gunner_hero)
        assert loc is not None
        hero_rect = loc.rect

        # Ogre AI + damage
        for slot in slots:
            if slot.alive and slot.creature is not None:
                ogre = slot.creature
                ogre.chase(hero_rect)
                ogre.tryclub(hero_rect, clubs)
                if pygame.sprite.spritecollide(ogre, shots, DOKILL):
                    ogre.bleed(blood)
                    ogre.life -= SHOT_DAMAGE
                    if ogre.life <= 0:
                        slot.alive = False
                        score.add_points(OGRE_KILL_POINTS)
                if pygame.sprite.spritecollide(ogre, pshots, DONTKILL):
                    ogre.bleed(blood)
                    ogre.life -= POWERSHOT_DAMAGE
                    if ogre.life <= 0:
                        slot.alive = False
                        score.add_points(OGRE_KILL_POINTS)
                if pygame.sprite.spritecollide(ogre, blade, DONTKILL):
                    ogre.bleed(blood)
                    ogre.life -= BLADE_DAMAGE
                    if ogre.life <= 0:
                        slot.alive = False
                        score.add_points(OGRE_KILL_POINTS)

        # Prof interactions
        if pygame.sprite.spritecollide(prof, ogres, DONTKILL):
            sprites.add(DialogText("Professor: (Sigh) Attack the subject, stupid ogres!"))
            ogres.empty()
            for slot in slots:
                slot.alive = False
                slot.creature = None

        if pygame.sprite.spritecollide(prof, heroes, DONTKILL):
            if score.score <= 9 and not checkmarks["talk_early"]:
                sprites.add(
                    DialogText("Professor: Attack the ogres, let me see what you can do!")
                )
                checkmarks["talk_early"] = True
            if score.score >= STAGE_ADVANCE_SCORE and not checkmarks["advance"]:
                sprites.add(
                    DialogText("Excellent work. What shall be your next challenge.. hm?")
                )
                checkmarks["advance"] = True
                ogres.empty()
                for slot in slots:
                    slot.alive = False
                    slot.creature = None
                from cyborg_fu.stages.stage_three import stage_three

                return stage_three(hero)

        # Render
        ogres.clear(screen, background)
        ogres.update()
        ogres.draw(screen)

        blood.clear(screen, background)
        blood.update()
        blood.draw(screen)

        shots.clear(screen, background)
        shots.update()
        shots.draw(screen)

        pshots.clear(screen, background)
        pshots.update()
        pshots.draw(screen)

        blade.clear(screen, background)
        blade.update()
        blade.draw(screen)

        clubs.clear(screen, background)
        clubs.update()
        clubs.draw(screen)

        sprites.clear(screen, background)
        sprites.update()
        sprites.draw(screen)

        pygame.display.flip()
```

- [ ] **Step 2: Commit**

```bash
git add cyborg_fu/stages/stage_two.py
git commit -m "feat: add Stage Two (Ogre battles) with bug fixes"
```

---

## Task 13: Stage Three

**Files:**
- Create: `cyborg_fu/stages/stage_three.py`

- [ ] **Step 1: Implement Stage Three**

Create `cyborg_fu/stages/stage_three.py` following the same pattern but with:
- Single Assassin boss + Shadow clones
- Block terrain forming the river boundary (reuse original block positions)
- Assassin AI: aim + shoot + dodge + shadow spawning
- Shadow taunts when player hits a decoy
- Victory dialog when assassin dies

```python
"""Stage Three: Boss battle against The Assassin."""

from __future__ import annotations

import random

import pygame
from pygame.locals import K_a, K_d, K_e, K_l, K_s, K_SPACE, K_w, KEYDOWN, KEYUP, QUIT

from cyborg_fu.constants import (
    ASSASSIN_BLADE_DAMAGE,
    ASSASSIN_PSHOT_DAMAGE,
    ASSASSIN_SHOT_DAMAGE_GUNNER,
    ASSASSIN_SHOT_DAMAGE_TESI,
    ASSASSIN_SHOT_HIT_DAMAGE,
    BLADE_COLLIDE_LATENCY,
    FPS,
    SHADOW_ODDS,
    SHADOW_SPAWN,
    SWING_COLLIDE_LATENCY,
    ASSASSIN_HIT_POINTS,
)
from cyborg_fu.creatures.assassin import Assassin
from cyborg_fu.creatures.base import Creature
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.shadow import Shadow
from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import Nature, State
from cyborg_fu.stages.base import create_image_background, create_screen
from cyborg_fu.ui.hud import LifeBar, ManaBar, Score
from cyborg_fu.ui.text import DialogText
from cyborg_fu.weapons.block import Block

DOKILL: bool = True
DONTKILL: bool = False

# River boundary block positions from original game
MIDDLE_BLOCKS: list[tuple[int, int]] = [
    (420, 10), (420, 40), (420, 80), (420, 120), (430, 160),
    (430, 200), (460, 240), (430, 280), (420, 310), (413, 400),
    (435, 434), (455, 456), (488, 488), (520, 496), (557, 503),
    (575, 536), (588, 564),
]
EAST_BLOCKS: list[tuple[int, int]] = [
    (464, 153), (504, 175), (543, 181), (574, 210), (575, 303),
    (570, 351), (544, 371), (524, 404), (495, 421),
]
WEST_BLOCKS: list[tuple[int, int]] = [
    (376, 188), (323, 202), (290, 213), (240, 220), (141, 209),
    (108, 163), (72, 148), (42, 133), (3, 121),
]

TAUNT_MESSAGES: list[str] = [
    "Assassin: What's the matter? Can't hit me? Haha!",
    "Assassin: Come on, stop trying to hit me and hit me!",
    "Assassin: What are you swinging at? I'm right here!",
    "Assassin: Bwahahahaha!",
    "Assassin: Super ketchup, premio tomato, catfish tuna.",
]


def stage_three(hero: str) -> str | None:
    """Run Stage Three: defeat The Assassin.

    Returns:
        None (game ends after this stage).
    """
    screen, screen_rect = create_screen()
    background = create_image_background("rivers.png", screen_rect)

    shots = pygame.sprite.Group()
    pshots = pygame.sprite.Group()
    ashots = pygame.sprite.Group()
    fakeshots = pygame.sprite.Group()
    shadows = pygame.sprite.Group()
    blade = pygame.sprite.Group()
    blood = pygame.sprite.Group()

    score = Score()
    assassin = Assassin(spawn=(100, 100), shot_group=ashots)
    text = DialogText("They sent 'The Assassin' for me! Please, defeat him!")

    tesi_hero: Tesi | None = None
    gunner_hero: Hero | None = None

    if hero == "tesi":
        tesi_hero = Tesi(blade)
        life_bar = LifeBar(tesi_hero)
        mana_bar = ManaBar(tesi_hero)
        heroes = pygame.sprite.Group(tesi_hero)
        objects = pygame.sprite.Group(tesi_hero, assassin, score, life_bar, mana_bar, text)
    else:
        gunner_hero = Hero(shots)
        life_bar = LifeBar(gunner_hero)
        mana_bar = ManaBar(gunner_hero)
        heroes = pygame.sprite.Group(gunner_hero)
        objects = pygame.sprite.Group(gunner_hero, assassin, score, life_bar, mana_bar, text)

    # Create terrain blocks
    all_block_positions = MIDDLE_BLOCKS + EAST_BLOCKS + WEST_BLOCKS
    block_sprites = [Block(pos) for pos in all_block_positions]
    blocks = pygame.sprite.Group(*block_sprites)
    first_block = block_sprites[0] if block_sprites else None

    gassassin = pygame.sprite.Group(assassin)

    checkmarks: dict[str, bool] = {"victory": False}

    screen.blit(background, (0, 0))
    pygame.display.flip()

    blade_available = 1
    collide_latency = 0
    shadowspawn = SHADOW_SPAWN
    shadow_alive = False
    current_shadow: Shadow | None = None

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        collide_latency -= 1

        active_hero = tesi_hero or gunner_hero
        assert active_hero is not None
        hero_rect = active_hero.rect

        assassin.aim(hero_rect, ashots)

        if shadow_alive and current_shadow is not None:
            current_shadow.aim(hero_rect, fakeshots)

        # Shadow spawning
        if shadowspawn > 0:
            shadowspawn -= 1
        elif not int(random.random() * SHADOW_ODDS):
            shadowspawn = SHADOW_SPAWN
            loc = assassin.rect.center
            facing = assassin.facing
            running = assassin.movepos.copy()
            current_shadow = Shadow(loc, fakeshots, facing, running)
            shadows.add(current_shadow)
            shadow_alive = True

        # Tesi input
        if hero == "tesi" and tesi_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        tesi_hero.healing = 1
                    if event.key == K_SPACE and blade_available == 1:
                        tesi_hero.throw(blade)
                        blade_available -= 1
                        collide_latency = BLADE_COLLIDE_LATENCY
                        assassin.dodge()
                    if event.key == K_w:
                        tesi_hero.moveup()
                    if event.key == K_s:
                        tesi_hero.movedown()
                    if event.key == K_a:
                        tesi_hero.moveleft()
                    if event.key == K_d:
                        tesi_hero.moveright()
                    if event.key == K_l and blade_available == 1:
                        tesi_hero.swing(blade)
                        collide_latency = SWING_COLLIDE_LATENCY
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        tesi_hero.state = State.STILL
                    if event.key == K_e:
                        tesi_hero.healing = 0

            if collide_latency <= 0:
                if pygame.sprite.spritecollide(tesi_hero, blade, DOKILL):
                    blade_available += 1

            if pygame.sprite.spritecollide(tesi_hero, ashots, DOKILL):
                tesi_hero.bleed(blood)
                tesi_hero.life -= ASSASSIN_SHOT_DAMAGE_TESI

        # Gunner input
        if hero == "gunner" and gunner_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        gunner_hero.powershot(pshots)
                    if event.key == K_SPACE:
                        gunner_hero.doublefire(shots)
                        assassin.dodge()
                    if event.key == K_w:
                        gunner_hero.moveup()
                    if event.key == K_s:
                        gunner_hero.movedown()
                    if event.key == K_a:
                        gunner_hero.moveleft()
                    if event.key == K_d:
                        gunner_hero.moveright()
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        gunner_hero.state = State.STILL

            if pygame.sprite.spritecollide(gunner_hero, ashots, DOKILL):
                gunner_hero.bleed(blood)
                gunner_hero.life -= ASSASSIN_SHOT_DAMAGE_GUNNER
                gunner_hero.knockback()

        # Shadow hit taunt
        if pygame.sprite.groupcollide(
            shadows, blade, DOKILL, DONTKILL
        ) or pygame.sprite.groupcollide(shadows, shots, DOKILL, DOKILL):
            msg = random.choice(TAUNT_MESSAGES)
            objects.add(DialogText(msg))
            shadows.empty()
            shadow_alive = False
            current_shadow = None

        # Assassin damage
        if pygame.sprite.spritecollide(assassin, blade, DONTKILL):
            assassin.bleed(blood)
            assassin.life -= ASSASSIN_BLADE_DAMAGE
            score.add_points(ASSASSIN_HIT_POINTS)

        if pygame.sprite.spritecollide(assassin, shots, DOKILL):
            assassin.bleed(blood)
            assassin.life -= ASSASSIN_SHOT_HIT_DAMAGE
            score.add_points(ASSASSIN_HIT_POINTS)

        if pygame.sprite.spritecollide(assassin, pshots, DONTKILL):
            assassin.bleed(blood)
            assassin.life -= ASSASSIN_PSHOT_DAMAGE
            score.add_points(ASSASSIN_HIT_POINTS)

        # Block collisions
        if first_block is not None:
            if pygame.sprite.groupcollide(blocks, heroes, DONTKILL, DONTKILL):
                first_block.collision(active_hero)
            if pygame.sprite.groupcollide(blocks, gassassin, DONTKILL, DONTKILL):
                first_block.collision(assassin)

        # Victory
        if assassin.life <= 0 and not checkmarks["victory"]:
            msg = "Professor: Incredible, you defeated 'The Assassin'! Yippie!"
            objects.add(DialogText(msg))
            checkmarks["victory"] = True

        # Render
        shadows.clear(screen, background)
        shadows.update()
        shadows.draw(screen)

        blood.clear(screen, background)
        blood.update()
        blood.draw(screen)

        shots.clear(screen, background)
        shots.update()
        shots.draw(screen)

        pshots.clear(screen, background)
        pshots.update()
        pshots.draw(screen)

        ashots.clear(screen, background)
        ashots.update()
        ashots.draw(screen)

        fakeshots.clear(screen, background)
        fakeshots.update()
        fakeshots.draw(screen)

        blade.clear(screen, background)
        blade.update()
        blade.draw(screen)

        objects.clear(screen, background)
        objects.update()
        objects.draw(screen)

        blocks.clear(screen, background)
        blocks.update()
        blocks.draw(screen)

        pygame.display.flip()
```

- [ ] **Step 2: Commit**

```bash
git add cyborg_fu/stages/stage_three.py
git commit -m "feat: add Stage Three (Assassin boss battle)"
```

---

## Task 14: Main Entry Point

**Files:**
- Modify: `cyborg_fu/__main__.py`

- [ ] **Step 1: Implement the main entry point**

Update `cyborg_fu/__main__.py`:
```python
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
```

- [ ] **Step 2: Verify the game launches**

```bash
source .venv/bin/activate
python -m cyborg_fu
```

Expected: game window opens with main menu.

- [ ] **Step 3: Commit**

```bash
git add cyborg_fu/__main__.py
git commit -m "feat: wire up main entry point with menu -> stage flow"
```

---

## Task 15: Image Asset Improvements

**Files:**
- Modify: various files in `data/`

- [ ] **Step 1: Convert colormap images to RGBA for proper transparency**

Many sprites use 8-bit colormap without alpha. Convert them to RGBA:

```bash
python -c "
from PIL import Image
import os

data_dir = 'data'
for name in os.listdir(data_dir):
    if name.endswith('.png'):
        path = os.path.join(data_dir, name)
        img = Image.open(path)
        if img.mode != 'RGBA':
            # Convert to RGBA, making the background color transparent
            rgba = img.convert('RGBA')
            datas = rgba.getdata()
            # Get the top-left pixel color as likely background
            bg = datas[0][:3]
            new_data = []
            for item in datas:
                if item[:3] == bg and name != 'graytile.png' and name != 'rivers.png':
                    new_data.append((item[0], item[1], item[2], 0))
                else:
                    new_data.append(item)
            rgba.putdata(new_data)
            rgba.save(path)
            print(f'Converted {name} to RGBA with transparency')
        else:
            print(f'{name} already RGBA')
"
```

Note: This requires `pip install Pillow`. If not available, skip this step - the game will still work with colormap images via pygame's `.convert()` / `.convert_alpha()`.

- [ ] **Step 2: Commit**

```bash
git add data/
git commit -m "feat: convert sprite images to RGBA with proper alpha transparency"
```

---

## Task 16: Remove Old Files

**Files:**
- Delete: all top-level `.py` files except any config

- [ ] **Step 1: Verify the new package works**

```bash
source .venv/bin/activate
python -m cyborg_fu
# Play briefly to confirm functionality
```

- [ ] **Step 2: Remove old source files**

```bash
git rm main.py mainmenu.py Creature.py Tesi.py Hero.py Runt.py Ogre.py \
       Assassin.py Shadow.py Blade.py ThrownBlade.py Shot.py PowerShot.py \
       Club.py Block.py Gun.py Blood.py DisplayObject.py StageOne.py \
       StageTwo.py StageThree.py
```

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove legacy Python 2 source files (replaced by cyborg_fu package)"
```

---

## Task 17: Comprehensive Test Suite

**Files:**
- Create/modify: multiple test files

- [ ] **Step 1: Add remaining test coverage**

Create `tests/test_stages/test_stage_two.py`:
```python
"""Tests for Stage Two logic."""

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
```

Create `tests/test_stages/test_stage_three.py`:
```python
"""Tests for Stage Three logic."""

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
```

Add additional weapon tests in `tests/test_weapons/test_thrown_blade.py`:
```python
"""Tests for ThrownBlade."""

from __future__ import annotations

from cyborg_fu.enums import Direction
from cyborg_fu.weapons.thrown_blade import ThrownBlade


class TestThrownBlade:
    def test_initial_clock(self) -> None:
        tb = ThrownBlade(position=(100, 100), facing=Direction.RIGHT)
        assert tb.clock == 1

    def test_all_directions(self) -> None:
        for direction, expected in [
            (Direction.RIGHT, [6, 0]),
            (Direction.LEFT, [-6, 0]),
            (Direction.UP, [0, -6]),
            (Direction.DOWN, [0, 6]),
        ]:
            tb = ThrownBlade(position=(100, 100), facing=direction)
            assert tb.movepos == expected, f"Failed for {direction}"
```

Add `tests/test_weapons/test_club.py`:
```python
"""Tests for Club weapon."""

from __future__ import annotations

import pygame

from cyborg_fu.enums import Direction
from cyborg_fu.weapons.club import Club


class TestClub:
    def test_lifetime(self) -> None:
        c = Club(position=(100, 100), facing=Direction.RIGHT)
        assert c.life == 10

    def test_dies_after_lifetime(self) -> None:
        c = Club(position=(100, 100), facing=Direction.RIGHT)
        group = pygame.sprite.Group(c)
        for _ in range(10):
            c.update()
        assert c not in group
```

Add `tests/test_weapons/test_power_shot.py`:
```python
"""Tests for PowerShot weapon."""

from __future__ import annotations

from cyborg_fu.enums import Direction
from cyborg_fu.weapons.power_shot import PowerShot


class TestPowerShot:
    def test_lifetime_longer_than_shot(self) -> None:
        ps = PowerShot(position=(100, 100), facing=Direction.RIGHT)
        assert ps.life == 65

    def test_all_directions(self) -> None:
        for direction in Direction:
            ps = PowerShot(position=(100, 100), facing=direction)
            assert ps.movepos != [0, 0]
```

- [ ] **Step 2: Run full test suite**

```bash
pytest tests/ -v --tb=short
```

Expected: all tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/
git commit -m "test: add comprehensive test suite for all game modules"
```

---

## Task 18: Pylint, Mypy, and Final Cleanup

**Files:**
- Modify: various files to resolve lint/type errors

- [ ] **Step 1: Run pylint and fix all errors**

```bash
pylint cyborg_fu/ --output-format=text 2>&1 | head -100
```

Common fixes needed:
- Add missing docstrings
- Fix any remaining naming convention issues
- Resolve any import order issues
- Handle any unused variable warnings

Fix each issue until:
```bash
pylint cyborg_fu/
```
Shows 10.00/10.

- [ ] **Step 2: Run mypy strict and fix all errors**

```bash
mypy cyborg_fu/ --strict 2>&1 | head -100
```

Common fixes:
- Add return type annotations to any missing functions
- Add explicit types to any `Any` usages
- Fix protocol type mismatches
- Handle pygame's untyped stubs

Fix each issue until:
```bash
mypy cyborg_fu/ --strict
```
Shows "Success: no issues found"

- [ ] **Step 3: Run the full test suite one final time**

```bash
pytest tests/ -v
```

All tests must pass.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "fix: resolve all pylint and mypy errors for zero-warning compliance"
```

---

## Task 19: README and Documentation

**Files:**
- Modify: `README` -> `README.md`

- [ ] **Step 1: Write comprehensive README**

Rename and rewrite `README` to `README.md`:

```markdown
# Cyborg-Fu

A pygame arcade fighting game where you play as a cyborg warrior battling through three stages of increasingly difficult enemies.

Originally written as a college assignment at DTU (Danish Technical University) in 2010, modernized to Python 3.13+ in 2026.

## Story

You are a cyborg created by a mad professor. He's completed your programming and wants to test you against his menagerie of creatures. Fight through three stages — Runts, Ogres, and the deadly Assassin — to prove your worth.

## Requirements

- Python 3.13 or later
- pygame-ce (installed automatically)

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd cyborg-fu

# Create virtual environment
python3.13 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install
pip install -e .
```

## Running the Game

```bash
source .venv/bin/activate
python -m cyborg_fu
```

## Controls

| Key | Action |
|-----|--------|
| W/A/S/D | Move Up/Left/Down/Right |
| Space | Primary attack (throw blade / double-fire) |
| L | Melee swing (Tesi only) |
| E | Heal (Tesi) / Power Shot (Gunner) |

## Heroes

**Tesi (Sword)** - 300 HP. Throws and swings a blade. Can heal using mana.

**Gunner (Gun)** - 100 HP. Fires twin bullets. Can use mana-powered shots.

## Stages

1. **Runts** - Small wandering enemies. Score 10 points, then talk to the Professor.
2. **Ogres** - Tough enemies that chase you and swing clubs. Score 10 points to advance.
3. **The Assassin** - Final boss who shoots at you and spawns shadow decoys.

## Development

```bash
# Install dev dependencies
pip install pytest pylint mypy

# Run tests
pytest tests/ -v

# Run linter
pylint cyborg_fu/

# Run type checker
mypy cyborg_fu/ --strict
```

## License

MIT License - Copyright (c) 2010 Stephen Sanchez
```

- [ ] **Step 2: Remove old README and commit**

```bash
git rm README
git add README.md
git commit -m "docs: add comprehensive README with install, controls, and dev instructions"
```

---

## Summary of Bug Fixes

| Bug | Task | Description |
|-----|------|-------------|
| B1 | Task 3 | Created missing `health.png` and `mana.png` assets |
| B2 | Task 11 | Fixed runt slot C checking wrong alive variable |
| B3 | Task 8 | Blood particles now actually scatter from hit position |
| B4 | Task 9 | `Score.plus(int)` renamed to `add_points(points)` |
| B5 | Task 11-13 | ManaBar properly added to sprite groups in all stages |
| B6 | Task 4 | `doublefire()` uses if/else to prevent unbound variables |
| B7 | Task 4 | Knockback now pushes opposite to facing direction |
| B8 | Task 16 | Python 2 `raise` syntax removed (old files deleted) |
| B9 | Task 16 | Python 2 `except` syntax removed (old files deleted) |
| B10 | Task 16 | Python 2 `print` statement removed (old files deleted) |
