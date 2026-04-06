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
