"""Stage Three: Boss Battle against the Assassin."""
from __future__ import annotations
import random
from dataclasses import dataclass, field
import pygame
from pygame.locals import K_a, K_d, K_e, K_l, K_s, K_SPACE, K_w, KEYDOWN, KEYUP, QUIT
from cyborg_fu.constants import (
    ASSASSIN_BLADE_DAMAGE, ASSASSIN_PSHOT_DAMAGE, ASSASSIN_SHOT_DAMAGE_GUNNER,
    ASSASSIN_SHOT_DAMAGE_TESI, ASSASSIN_SHOT_HIT_DAMAGE, ASSASSIN_HIT_POINTS,
    BLADE_COLLIDE_LATENCY, BLADE_DAMAGE, FPS, POWERSHOT_DAMAGE,
    SHADOW_ODDS, SHADOW_SPAWN, SHOT_DAMAGE, SWING_COLLIDE_LATENCY,
)
from cyborg_fu.creatures.assassin import Assassin
from cyborg_fu.creatures.hero import Hero
from cyborg_fu.creatures.shadow import Shadow
from cyborg_fu.creatures.tesi import Tesi
from cyborg_fu.enums import State
from cyborg_fu.stages.base import create_screen, create_image_background
from cyborg_fu.ui.hud import LifeBar, ManaBar, Score
from cyborg_fu.ui.text import DialogText
from cyborg_fu.weapons.block import Block

DOKILL: bool = True
DONTKILL: bool = False

MIDDLE_BLOCKS = [
    (420, 10), (420, 40), (420, 80), (420, 120), (430, 160),
    (430, 200), (460, 240), (430, 280), (420, 310), (413, 400),
    (435, 434), (455, 456), (488, 488), (520, 496), (557, 503),
    (575, 536), (588, 564),
]
EAST_BLOCKS = [
    (464, 153), (504, 175), (543, 181), (574, 210), (575, 303),
    (570, 351), (544, 371), (524, 404), (495, 421),
]
WEST_BLOCKS = [
    (376, 188), (323, 202), (290, 213), (240, 220), (141, 209),
    (108, 163), (72, 148), (42, 133), (3, 121),
]

TAUNT_MESSAGES = [
    "Assassin: What's the matter? Can't hit me? Haha!",
    "Assassin: Come on, stop trying to hit me and hit me!",
    "Assassin: What are you swinging at? I'm right here!",
    "Assassin: Bwahahahaha!",
    "Assassin: Super ketchup, premio tomato, catfish tuna.",
]


def stage_three(hero: str) -> str | None:
    """Run Stage Three. Returns None when finished or quit."""
    screen, screen_rect = create_screen()
    background = create_image_background("river.png", screen_rect)

    shots = pygame.sprite.Group()
    pshots = pygame.sprite.Group()
    blade = pygame.sprite.Group()
    blood = pygame.sprite.Group()
    assassin_shots = pygame.sprite.Group()
    shadows = pygame.sprite.Group()

    # Build block groups
    all_blocks = pygame.sprite.Group()
    for pos in MIDDLE_BLOCKS + EAST_BLOCKS + WEST_BLOCKS:
        all_blocks.add(Block(pos))

    assassin = Assassin(spawn=(600, 200), shot_group=assassin_shots)
    score = Score()
    text = DialogText("Assassin: You dare challenge me?!")

    tesi_hero: Tesi | None = None
    gunner_hero: Hero | None = None

    if hero == "tesi":
        tesi_hero = Tesi(blade)
        life_bar = LifeBar(tesi_hero)
        mana_bar = ManaBar(tesi_hero)
        heroes = pygame.sprite.Group(tesi_hero)
        sprites = pygame.sprite.Group(tesi_hero, assassin, score, life_bar, mana_bar, text)
    else:
        gunner_hero = Hero(shots)
        life_bar = LifeBar(gunner_hero)
        mana_bar = ManaBar(gunner_hero)
        heroes = pygame.sprite.Group(gunner_hero)
        sprites = pygame.sprite.Group(gunner_hero, assassin, score, life_bar, mana_bar, text)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    blade_available = 1
    collide_latency = 0
    shadow_timer = SHADOW_SPAWN

    while True:
        clock.tick(FPS)
        collide_latency -= 1

        # Shadow spawn timer
        shadow_timer -= 1
        if shadow_timer <= 0:
            shadow_timer = SHADOW_SPAWN
            if not int(random.random() * SHADOW_ODDS):
                new_shadow = Shadow(
                    spawn=(assassin.rect.x, assassin.rect.y),
                    shot_group=assassin_shots,
                    facing=assassin.facing,
                    running=list(assassin.movepos),
                )
                shadows.add(new_shadow)
                sprites.add(new_shadow)

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
                        assassin.dodge()
                elif event.type == KEYUP:
                    if event.key in (K_a, K_d, K_w, K_s):
                        tesi_hero.state = State.STILL
                    if event.key == K_e:
                        tesi_hero.healing = 0

            if collide_latency <= 0:
                if pygame.sprite.spritecollide(tesi_hero, blade, DOKILL):
                    blade_available += 1

            # Assassin shots hitting tesi
            if pygame.sprite.spritecollide(tesi_hero, assassin_shots, DOKILL):
                tesi_hero.bleed(blood)
                tesi_hero.life -= ASSASSIN_SHOT_DAMAGE_TESI

            # Block collisions
            for block in pygame.sprite.spritecollide(tesi_hero, all_blocks, DONTKILL):
                block.collision(tesi_hero)

        # Gunner input/combat
        if hero == "gunner" and gunner_hero is not None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        gunner_hero.powershot(pshots)
                        assassin.dodge()
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

            # Assassin shots hitting gunner
            if pygame.sprite.spritecollide(gunner_hero, assassin_shots, DOKILL):
                gunner_hero.bleed(blood)
                gunner_hero.life -= ASSASSIN_SHOT_DAMAGE_GUNNER
                gunner_hero.knockback()

            # Block collisions
            for block in pygame.sprite.spritecollide(gunner_hero, all_blocks, DONTKILL):
                block.collision(gunner_hero)

        # Assassin AI
        if hero == "tesi" and tesi_hero is not None:
            assassin.aim(tesi_hero.rect, assassin_shots)
        elif hero == "gunner" and gunner_hero is not None:
            assassin.aim(gunner_hero.rect, assassin_shots)

        # Block collision for assassin
        for block in pygame.sprite.spritecollide(assassin, all_blocks, DONTKILL):
            block.collision(assassin)

        # Damage to assassin from player weapons
        if pygame.sprite.spritecollide(assassin, shots, DOKILL):
            assassin.bleed(blood)
            assassin.life -= SHOT_DAMAGE
            score.add_points(ASSASSIN_HIT_POINTS)
        if pygame.sprite.spritecollide(assassin, pshots, DONTKILL):
            assassin.bleed(blood)
            assassin.life -= ASSASSIN_PSHOT_DAMAGE
            score.add_points(ASSASSIN_HIT_POINTS)
        if pygame.sprite.spritecollide(assassin, blade, DONTKILL):
            assassin.bleed(blood)
            assassin.life -= BLADE_DAMAGE
            score.add_points(ASSASSIN_HIT_POINTS)

        # Damage to shadows
        hit_shadows = pygame.sprite.groupcollide(
            shadows, shots, DONTKILL, DOKILL
        )
        for shadow in hit_shadows:
            shadow.bleed(blood)
            shadow.life -= ASSASSIN_SHOT_HIT_DAMAGE
            sprites.add(DialogText(random.choice(TAUNT_MESSAGES)))

        hit_shadows_blade = pygame.sprite.groupcollide(
            shadows, blade, DONTKILL, DONTKILL
        )
        for shadow in hit_shadows_blade:
            shadow.bleed(blood)
            shadow.life -= ASSASSIN_BLADE_DAMAGE
            sprites.add(DialogText(random.choice(TAUNT_MESSAGES)))

        # Victory condition
        if assassin.life <= 0:
            sprites.add(DialogText("You have defeated the Assassin! Victory!"))
            sprites.update()
            sprites.draw(screen)
            pygame.display.flip()
            pygame.time.wait(3000)
            return hero

        # Render
        all_blocks.clear(screen, background)
        all_blocks.update()
        all_blocks.draw(screen)
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
        assassin_shots.clear(screen, background)
        assassin_shots.update()
        assassin_shots.draw(screen)
        sprites.clear(screen, background)
        sprites.update()
        sprites.draw(screen)
        pygame.display.flip()
