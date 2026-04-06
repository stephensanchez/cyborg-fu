"""Base Creature class for all game characters."""

from __future__ import annotations

import random

import pygame

from cyborg_fu.assets import load_png
from cyborg_fu.constants import (
    DEFAULT_MAX_LIFE,
    DEFAULT_MAX_MANA,
    HEAL_LIFE_GAIN,
    HEAL_MANA_COST,
    HEAL_RADIUS,
    HEAL_CIRCLE_WIDTH,
    KNOCKBACK_FORCE,
    POWERSHOT_MANA_COST,
    WALL_MARGIN,
    COLOR_HEAL_GREEN,
    COLOR_HEAL_BLUE,
)
from cyborg_fu.enums import Direction, Nature, State


class Creature(pygame.sprite.Sprite):
    """Base class for all game sprites (heroes and enemies)."""

    def __init__(
        self,
        nature: Nature,
        spawn: tuple[int, int],
        speed: tuple[int, int],
        life: int,
        graphic: str,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.nature = nature
        self.spawn = spawn
        self.speed = speed
        self.life = life
        self.graphic = graphic

        self.facing: Direction = Direction.RIGHT
        self.state: State = State.STILL
        self.counter: int = 100
        self.shotcounter: int = 5
        self.clubcounter: int = 10
        self.mana: int = DEFAULT_MAX_MANA
        self.healing: int = 0
        self.attack: pygame.sprite.Group = pygame.sprite.Group()

        self.image, self.rect = load_png(graphic)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self._reinit()

    def _reinit(self) -> None:
        """Reset position and movement state."""
        self.state = State.STILL
        self.movepos: list[int] = [0, 0]
        firstpos = self.rect.move(self.spawn)
        if self.area.contains(firstpos):
            self.rect = firstpos
        self.original = self.image

    def update(self) -> None:
        """Update creature state each frame."""
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

    def moveup(self) -> None:
        """Move the creature upward."""
        self.movepos[1] = self.movepos[1] - self.speed[1]
        self.state = State.MOVE_UP
        self.turn(Direction.UP)

    def movedown(self) -> None:
        """Move the creature downward."""
        self.movepos[1] = self.movepos[1] + self.speed[1]
        self.state = State.MOVE_DOWN
        self.turn(Direction.DOWN)

    def moveleft(self) -> None:
        """Move the creature left."""
        self.movepos[0] = self.movepos[0] - self.speed[0]
        self.state = State.MOVE_LEFT
        self.turn(Direction.LEFT)

    def moveright(self) -> None:
        """Move the creature right."""
        self.movepos[0] = self.movepos[0] + self.speed[0]
        self.state = State.MOVE_RIGHT
        self.turn(Direction.RIGHT)

    def turn(self, facing: Direction) -> None:
        """Rotate the sprite image to face the given direction."""
        self.facing = facing
        self.image = pygame.transform.rotate(self.original, facing.rotation)

    def bleed(self, bloodgroup: pygame.sprite.Group) -> None:
        """Spawn a blood effect at this creature's position."""
        from cyborg_fu.effects.blood import Blood  # lazy import to avoid circular deps

        new_blood = Blood(self.rect.center)
        bloodgroup.add(new_blood)

    def knockback(self) -> None:
        """Push the creature opposite to its facing direction (B7 fix).

        BUG B7: Original code pushed in the FACING direction (into danger).
        Fixed: push in the OPPOSITE direction.
        """
        self.state = State.STILL
        opposite = self.facing.opposite
        if opposite is Direction.UP:
            self.movepos[1] -= KNOCKBACK_FORCE
        elif opposite is Direction.DOWN:
            self.movepos[1] += KNOCKBACK_FORCE
        elif opposite is Direction.LEFT:
            self.movepos[0] -= KNOCKBACK_FORCE
        elif opposite is Direction.RIGHT:
            self.movepos[0] += KNOCKBACK_FORCE
        self.rect = self.rect.move(self.movepos)

    def _off_wall(self) -> None:
        """Reverse movement if the creature hits a wall boundary."""
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

    def aim(
        self, target_rect: pygame.Rect, shot_group: pygame.sprite.Group
    ) -> None:
        """AI: aim at target and fire periodically."""
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
        """AI: swing club at target if close enough."""
        xdiff = target_rect[0] - self.rect[0]
        ydiff = target_rect[1] - self.rect[1]
        self.clubcounter -= 1
        if self.clubcounter == 0:
            self.clubcounter = 10
            if int(random.random() * 100):
                if xdiff < 65 and xdiff > -65 and ydiff < 65 and ydiff > -65:
                    self._swing_club(club_group)

    def _swing_club(self, club_group: pygame.sprite.Group) -> None:
        """Spawn a club weapon sprite."""
        from cyborg_fu.weapons.club import Club  # lazy import

        self.state = State.STILL
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
        """AI: randomly jump slightly to avoid attacks."""
        choice = random.choice(range(1, 17))
        dodges = {
            1: [0, 2],
            2: [0, -2],
            3: [2, 0],
            4: [-2, 0],
            5: [2, 2],
            6: [-4, 4],
            7: [4, -4],
            8: [-4, -4],
        }
        if choice in dodges:
            self.movepos = dodges[choice]

    def _wanderer(self) -> None:
        """AI: random wandering behavior for runts and assassins."""
        self.counter -= 1
        if self.counter == 0:
            self.counter = 100
            self.state = State.STILL
            if int(random.random() * 100):
                choice = random.choice((1, 2, 3, 4, 5))
                self.movepos = [0, 0]
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

    def swing(self, bladegroup: pygame.sprite.Group) -> None:
        """Swing a blade weapon."""
        from cyborg_fu.weapons.blade import Blade  # lazy import

        self.state = State.STILL
        new_blade = Blade(self.rect.center, self.facing)
        bladegroup.add(new_blade)

    def throw(self, bladegroup: pygame.sprite.Group) -> None:
        """Throw a blade weapon."""
        from cyborg_fu.weapons.thrown_blade import ThrownBlade  # lazy import

        new_thrown = ThrownBlade(self.rect.midtop, self.facing)
        bladegroup.add(new_thrown)

    def _fire(self, shotgroup: pygame.sprite.Group) -> None:
        """Fire a single shot."""
        from cyborg_fu.weapons.shot import Shot  # lazy import

        new_shot = Shot(self.rect.midtop, self.facing)
        shotgroup.add(new_shot)

    def doublefire(self, shotgroup: pygame.sprite.Group) -> None:
        """Fire two shots side-by-side.

        BUG B6 FIX: Original used two independent `if` blocks, leaving
        firstShot/secondShot potentially unbound. Fixed with if/else.
        """
        from cyborg_fu.weapons.shot import Shot  # lazy import

        if self.facing in (Direction.RIGHT, Direction.LEFT):
            first_shot = Shot(self.rect.midtop, self.facing)
            second_shot = Shot(self.rect.midbottom, self.facing)
        else:
            # UP or DOWN
            first_shot = Shot(self.rect.midleft, self.facing)
            second_shot = Shot(self.rect.midright, self.facing)
        shotgroup.add(first_shot)
        shotgroup.add(second_shot)

    def powershot(self, shotgroup: pygame.sprite.Group) -> None:
        """Fire a powerful double shot if enough mana is available."""
        from cyborg_fu.weapons.power_shot import PowerShot  # lazy import

        if self.mana > POWERSHOT_MANA_COST - 1:
            self.mana -= POWERSHOT_MANA_COST
            if self.facing in (Direction.RIGHT, Direction.LEFT):
                first_shot = PowerShot(self.rect.midtop, self.facing)
                second_shot = PowerShot(self.rect.midbottom, self.facing)
            else:
                first_shot = PowerShot(self.rect.midleft, self.facing)
                second_shot = PowerShot(self.rect.midright, self.facing)
            shotgroup.add(first_shot)
            shotgroup.add(second_shot)

    def regen(self) -> None:
        """Regenerate mana over time."""
        choice = random.choice((1, 2, 3, 4, 5))
        if choice == 1 and self.mana < DEFAULT_MAX_MANA:
            self.mana += 1

    def heal(self) -> None:
        """Heal life using mana (Tesi ability)."""
        screen = pygame.display.get_surface()
        pos = self.rect.center
        color = random.choice((COLOR_HEAL_GREEN, COLOR_HEAL_BLUE))
        if self.healing == 1:
            if self.mana > HEAL_MANA_COST - 1 and self.life < DEFAULT_MAX_LIFE:
                self.state = State.STILL
                self.mana -= HEAL_MANA_COST
                self.life += HEAL_LIFE_GAIN
                pygame.draw.circle(screen, color, pos, HEAL_RADIUS, HEAL_CIRCLE_WIDTH)
