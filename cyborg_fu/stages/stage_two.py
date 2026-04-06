"""Stage Two: Fight the Ogres."""
from __future__ import annotations
import random
from dataclasses import dataclass
import pygame
from pygame.locals import K_a, K_d, K_e, K_l, K_s, K_SPACE, K_w, KEYDOWN, KEYUP, QUIT
from cyborg_fu.constants import (
    BLADE_COLLIDE_LATENCY, BLADE_DAMAGE, FPS, OGRE_CLUB_DAMAGE_GUNNER,
    OGRE_CLUB_DAMAGE_TESI, OGRE_KILL_POINTS, OGRE_ODDS, OGRE_RELOAD,
    POWERSHOT_DAMAGE, RUNT_CONTACT_DAMAGE_GUNNER, RUNT_CONTACT_DAMAGE_TESI,
    SHOT_DAMAGE, STAGE_ADVANCE_SCORE, SWING_COLLIDE_LATENCY,
)
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.ogre import Ogre
from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import State
from cyborg_fu.stages.base import create_screen, create_tiled_background
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
    """Run Stage Two. Returns hero type for next stage or None if quit."""
    screen, screen_rect = create_screen()
    background = create_tiled_background("graytile.png", screen_rect)

    shots = pygame.sprite.Group()
    pshots = pygame.sprite.Group()
    blade = pygame.sprite.Group()
    blood = pygame.sprite.Group()
    clubs = pygame.sprite.Group()
    ogres = pygame.sprite.Group()

    score = Score()
    text = DialogText("Professor: These runts are much stronger!")

    tesi_hero: Tesi | None = None
    gunner_hero: Hero | None = None

    if hero == "tesi":
        tesi_hero = Tesi(blade)
        life_bar = LifeBar(tesi_hero)
        mana_bar = ManaBar(tesi_hero)
        heroes = pygame.sprite.Group(tesi_hero)
        sprites = pygame.sprite.Group(tesi_hero, score, life_bar, mana_bar, text)
    else:
        gunner_hero = Hero(shots)
        life_bar = LifeBar(gunner_hero)
        mana_bar = ManaBar(gunner_hero)
        heroes = pygame.sprite.Group(gunner_hero)
        sprites = pygame.sprite.Group(gunner_hero, score, life_bar, mana_bar, text)

    slots = [
        OgreSlot(spawn=(100, 50)),
        OgreSlot(spawn=(500, 50)),
    ]

    checkmarks: dict[str, bool] = {"advance": False}

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    blade_available = 1
    collide_latency = 0
    ogrereload = OGRE_RELOAD

    while True:
        clock.tick(FPS)
        collide_latency -= 1

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

        # Tesi input/combat
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
                        for slot in slots:
                            if slot.alive and slot.creature is not None:
                                slot.creature.dodge()
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        tesi_hero.state = State.STILL
                    if event.key == K_e:
                        tesi_hero.healing = 0

            if collide_latency <= 0:
                if pygame.sprite.spritecollide(tesi_hero, blade, DOKILL):
                    blade_available += 1

            if pygame.sprite.spritecollide(tesi_hero, clubs, DOKILL):
                tesi_hero.bleed(blood)
                tesi_hero.life -= OGRE_CLUB_DAMAGE_TESI

        # Gunner input/combat
        if hero == "gunner" and gunner_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        gunner_hero.powershot(pshots)
                        for slot in slots:
                            if slot.alive and slot.creature is not None:
                                slot.creature.dodge()
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

            if pygame.sprite.spritecollide(gunner_hero, clubs, DOKILL):
                gunner_hero.bleed(blood)
                gunner_hero.life -= OGRE_CLUB_DAMAGE_GUNNER
                gunner_hero.knockback()

        # Ogre AI and damage from weapons
        for slot in slots:
            if slot.alive and slot.creature is not None:
                ogre = slot.creature

                # Ogre chases and tries to club hero
                if hero == "tesi" and tesi_hero is not None:
                    ogre.chase(tesi_hero.rect)
                    ogre.tryclub(tesi_hero.rect, clubs)
                elif hero == "gunner" and gunner_hero is not None:
                    ogre.chase(gunner_hero.rect)
                    ogre.tryclub(gunner_hero.rect, clubs)

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

        # Stage advance check
        if score.score >= STAGE_ADVANCE_SCORE and not checkmarks["advance"]:
            sprites.add(DialogText("You defeated the ogres! Prepare for the final challenge!"))
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
