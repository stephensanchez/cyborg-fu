#!/usr/bin/env python
#The makings of my own Network RPG
#Many ideas come to mind but who knows how the game will play...

import pygame
import random
from pygame.locals import *
import os
from sprites import *
from aweapons import *
from main import *

dokill = 1
dontkill = 0
SCREENRECT = Rect(0, 0, 800, 600)
SCORE = 0      #Score update
SHADOW_SPAWN = 200
SHADOW_ODDS = 100

def assassin(hero, winstyle = 0):

        # Initialize screen
        pygame.init()
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        pygame.display.set_caption('Cyborg-Fu!')

        # Creating Background
        bgdtile = load_image('rivers.png')
        background = pygame.Surface(SCREENRECT.size)
        background.blit(bgdtile, (0,0))

        #Missle & Attack object groups must be determined before characters.
        shots = pygame.sprite.Group()
        pshots = pygame.sprite.Group()
        ashots = pygame.sprite.Group()
        fakeshots = pygame.sprite.Group()
        shadows = pygame.sprite.Group()
        blade = pygame.sprite.Group()
        blood = pygame.sprite.Group()

        #Scoreboard
        score = Score()
        scoresprite = pygame.sprite.RenderPlain(score)

        assassin = Assassin([100, 100], ashots)
        Shadow([100,300], fakeshots, "left", [0,0])

        #Text
        TEXT = "They sent an 'The Assassin' for me! Please, defeat him!"
        text = Text(TEXT)
        
        
        #Create Characters
        global tesi
        global gunner
        if hero == "tesi":
                tesi = Tesi(blade)
                life = Life(tesi)
                lifesprite = pygame.sprite.RenderPlain(life)
                heroes = pygame.sprite.Group(tesi)
                objects = pygame.sprite.Group(tesi, assassin, score, life, text)
        if hero == "gunner":
                gunner = Hero(shots)
                life = Life(gunner)
                lifesprite = pygame.sprite.RenderPlain(life)
                heroes = pygame.sprite.Group(gunner)
                objects = pygame.sprite.Group(gunner, assassin, score, life, text)

        #Creating an impassable block! Excitement abounds!
        #Block works! Now to map out the river!
        middle = Block([420, 10])
        middle1 = Block([420, 40])
        middle2 = Block([420, 80])
        middle3 = Block([420, 120])
        middle4 = Block([430, 160])
        middle5 = Block([430, 200])
        middle6 = Block([460, 240])
        middle7 = Block([430, 280])
        middle8 = Block([420, 310])
        middle9 = Block([413, 400])
        middle10 = Block([435, 434])
        middle11 = Block([455, 456])
        middle12 = Block([488, 488])
        middle13 = Block([520, 496])
        middle14 = Block([557, 503])
        middle15 = Block([575, 536])
        middle16 = Block([588, 564])
        east1 = Block([464, 153])
        east2 = Block([504, 175])
        east3 = Block([543, 181])
        east4 = Block([574, 210])
        east5 = Block([575, 303])
        east6 = Block([570, 351])
        east7 = Block([544, 371])
        east8 = Block([524, 404])
        east9 = Block([495, 421])
        west1 = Block([376, 188])
        west2 = Block([323, 202])
        west3 = Block([290, 213])
        west4 = Block([240, 220])
        west5 = Block([141, 209])
        west6 = Block([108, 163])
        west7 = Block([72, 148])
        west8 = Block([42, 133])
        west9 = Block([3, 121])
        
        #Checkmarks to avoid repeating text
        CHECKMARK1 = 0
        CHECKMARK2 = 0
        
        #Create Game Groups
        gassassin = pygame.sprite.Group(assassin)
        blocks = pygame.sprite.Group(middle, middle1, middle2,
                                     middle3, middle4, middle5,
                                     middle6, middle7, middle8,
                                     middle9, middle10, middle11,
                                     middle12, middle13, middle14,
                                     middle15, middle16, east1,
                                     east2, east3, east4, east5,
                                     east6, east7, east8, east9,
                                     west1, west2, west3, west4,
                                     west5, west6, west7, west8,
                                     west9)
        
        #Default groups for each sprite class
        Shot.containers = shots
        Pshot.containers = pshots
        Shadow.containers = shadows
        
        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        #Tesi's blade
        BLADE = 1
        COLLIDELATENCY = 0

        #Assassin creates an illusional shadow
        shadowspawn = SHADOW_SPAWN
        SALIVE = 0

        # Initialise clock
        clock = pygame.time.Clock()

        # Event loop
        while 1:
            
                clock.tick(60)

                COLLIDELATENCY = COLLIDELATENCY - 1
                if hero == "tesi":
                        loc = tesi.rect
                if hero == "gunner":
                        loc = gunner.rect
                        
                assassin.aim(loc)

                if SALIVE == 1:
                        shadow.aim(loc)

                if shadowspawn > 0:
                        shadowspawn = shadowspawn - 1
                elif not int(random.random() * SHADOW_ODDS):
                        shadowspawn = SHADOW_SPAWN
                        loc = assassin.rect.center
                        facing = assassin.facing
                        running = assassin.movepos
                        shadow = Shadow(loc, fakeshots, facing, running)
                        shadows.add(shadow)
                        SALIVE = 1
                            
                if hero == "tesi":
                        for event in pygame.event.get():
                                if event.type == QUIT: 
                                        pygame.quit()
                                        return
                                if event.type == KEYDOWN:
                                        if event.key == K_e:
                                                tesi.healing = 1
                                        if event.key == K_SPACE:
                                                if BLADE == 1:
                                                        tesi.throw(blade)
                                                        BLADE = BLADE - 1
                                                        COLLIDELATENCY = 60
                                                        assassin.dodge()
                                        if event.key == K_w:
                                                tesi.moveup()
                                        if event.key == K_s:
                                                tesi.movedown()
                                        if event.key == K_a:
                                                tesi.moveleft()
                                        if event.key == K_d:
                                                tesi.moveright()
                                        if event.key == K_l:
                                                if BLADE == 1:
                                                        tesi.swing(blade)
                                                        COLLIDELATENCY = 150
                                elif event.type == KEYUP:
                                        if event.key == K_e:
                                                tesi.healing = 0
                                        if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                                                tesi.state = "still"

                        # Tesi gets his blade back
                        if COLLIDELATENCY <= 0:
                                if pygame.sprite.spritecollide(tesi, blade, dokill):
                                        BLADE = BLADE + 1

                        if pygame.sprite.spritecollide(tesi, ashots, dokill):
                                tesi.bleed(blood)
                                tesi.life = tesi.life - 6


                if hero == "gunner":
                        for event in pygame.event.get():
                                if event.type == QUIT: 
                                        pygame.quit()
                                        return
                                if event.type == KEYDOWN:
                                        if event.key == K_e:
                                                gunner.powershot(pshots)
                                        if event.key == K_SPACE:
                                                gunner.doublefire(shots)
                                                assassin.dodge()
                                                        
                                        if event.key == K_w:
                                                gunner.moveup()
                                        if event.key == K_s:
                                                gunner.movedown()
                                        if event.key == K_a:
                                                gunner.moveleft()
                                        if event.key == K_d:
                                                gunner.moveright()
                                elif event.type == KEYUP:
                                        if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                                                gunner.state = "still"


                        if pygame.sprite.spritecollide(gunner, ashots, dokill):
                                gunner.bleed(blood)
                                gunner.life = gunner.life - 10
                                gunner.knockback()
                      

                if pygame.sprite.groupcollide(shadows, blade, dokill, dontkill) or pygame.sprite.groupcollide(shadows, shots, dokill, dokill):
                        a = "Assassin: What's the matter? Can't hit me? Haha!"
                        b = "Assassin: Come on, stop trying to hit me and hit me!"
                        c = "Assassin: What are you swinging at? I'm right here!"
                        d = "Assassin: Bwahahahaha!"
                        e = "Assassin: Super ketchup, premio tomato, catfish tuna."
                        msg = random.choice((a, b, c, d, e))
                        newText = Text(msg)
                        objects.add(newText)
                        shadows.empty()
                        SALIVE = 0

                if pygame.sprite.spritecollide(assassin, blade, dontkill):
                        assassin.bleed(blood)
                        assassin.life = assassin.life - 2
                        score.plus(1)

                if pygame.sprite.spritecollide(assassin, shots, dokill):
                        assassin.bleed(blood)
                        assassin.life = assassin.life - 5
                        score.plus(1)

                if pygame.sprite.spritecollide(assassin, pshots, dontkill):
                        assassin.bleed(blood)
                        assassin.life = assassin.life - 8
                        score.plus(1)

                if pygame.sprite.groupcollide(blocks, heroes, dontkill, dontkill):
                        if hero == "tesi":
                                middle.collision(tesi)
                        if hero == "gunner":
                                middle.collision(gunner)

                if pygame.sprite.groupcollide(blocks, gassassin, dontkill, dontkill):
                        middle.collision(assassin)

                if assassin.life < 0:
                        if CHECKMARK1 == 0:
                                msg = "Professor: Incredible, you defeated 'The Assassin'! Yippie!"
                                newText = Text(msg)
                                objects.add(newText)
                                CHECKMARK1 = 1
                                

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

