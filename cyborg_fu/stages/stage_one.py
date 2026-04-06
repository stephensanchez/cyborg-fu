"""Stage One: Fight the Runts."""
from __future__ import annotations
import random
from dataclasses import dataclass
import pygame
from pygame.locals import K_a, K_d, K_e, K_l, K_s, K_SPACE, K_w, KEYDOWN, KEYUP, QUIT
from cyborg_fu.constants import (
    BLADE_COLLIDE_LATENCY, BLADE_DAMAGE, FPS, POWERSHOT_DAMAGE,
    RUNT_CONTACT_DAMAGE_GUNNER, RUNT_CONTACT_DAMAGE_TESI, RUNT_KILL_POINTS,
    RUNT_ODDS, RUNT_RELOAD, SHOT_DAMAGE, STAGE_ADVANCE_SCORE, SWING_COLLIDE_LATENCY,
)
from cyborg_fu.creatures.base import Creature
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.runt import Runt
from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import Nature, State
from cyborg_fu.stages.base import create_screen, create_tiled_background
from cyborg_fu.ui.hud import LifeBar, ManaBar, Score
from cyborg_fu.ui.text import DialogText

DOKILL: bool = True
DONTKILL: bool = False


@dataclass
class EnemySlot:
    """Tracks a single enemy spawn slot. Bug B2 fix: independent tracking."""

    spawn: tuple[int, int]
    alive: bool = False
    creature: Runt | None = None


def stage_one(hero: str) -> str | None:
    """Run Stage One. Returns hero type for next stage or None if quit."""
    screen, screen_rect = create_screen()
    background = create_tiled_background("graytile.png", screen_rect)

    shots = pygame.sprite.Group()
    pshots = pygame.sprite.Group()
    blade = pygame.sprite.Group()
    blood = pygame.sprite.Group()
    runties = pygame.sprite.Group()

    prof = Creature(nature=Nature.PROF, spawn=(740, 30), speed=(1, 1), life=10, graphic="prof.png")
    score = Score()
    text = DialogText("Professor: Let's see what they can do...")

    tesi_hero: Tesi | None = None
    gunner_hero: Hero | None = None

    if hero == "tesi":
        tesi_hero = Tesi(blade)
        life_bar = LifeBar(tesi_hero)
        mana_bar = ManaBar(tesi_hero)  # Bug B5 fix: capture mana_bar
        heroes = pygame.sprite.Group(tesi_hero)
        sprites = pygame.sprite.Group(tesi_hero, prof, score, life_bar, mana_bar, text)
    else:
        gunner_hero = Hero(shots)
        life_bar = LifeBar(gunner_hero)
        mana_bar = ManaBar(gunner_hero)  # Bug B5 fix
        heroes = pygame.sprite.Group(gunner_hero)
        sprites = pygame.sprite.Group(gunner_hero, prof, score, life_bar, mana_bar, text)

    # Bug B2 fix: use independent EnemySlot objects
    slots = [
        EnemySlot(spawn=(100, 50)),
        EnemySlot(spawn=(200, 50)),
        EnemySlot(spawn=(300, 50)),
        EnemySlot(spawn=(400, 50)),
        EnemySlot(spawn=(500, 50)),
    ]

    checkmarks: dict[str, bool] = {"score4": False, "talk_early": False, "advance": False}

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    blade_available = 1
    collide_latency = 0
    runtreload = RUNT_RELOAD

    while True:
        clock.tick(FPS)
        collide_latency -= 1

        # Dialog at score 4
        if score.score == 4 and not checkmarks["score4"]:
            sprites.add(DialogText("Professor: Hmm, they seem to be working properly. Excellent!"))
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

        # Gunner input/combat
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

        # Runt damage from weapons
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
                sprites.add(DialogText("Professor: Attack the runts, let me see what you can do!"))
                checkmarks["talk_early"] = True
            if score.score >= STAGE_ADVANCE_SCORE and not checkmarks["advance"]:
                sprites.add(DialogText("I have finally succeeded. I shall call off these runts."))
                checkmarks["advance"] = True
                runties.empty()
                for slot in slots:
                    slot.alive = False
                    slot.creature = None
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
