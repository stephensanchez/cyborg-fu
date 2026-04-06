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
