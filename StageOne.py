#!/usr/bin/env python
#Cyborg-Fu
#Many ideas come to mind but who knows how the game will play...

import pygame
import random
from StageTwo import *
from pygame.locals import *
from main import *
from Runt import Runt
from Tesi import Tesi
from Hero import Hero
from Creature import Creature
from Shot import Shot
from PowerShot import PowerShot


dokill = 1
dontkill = 0
SCREENRECT = Rect(0, 0, 800, 600)
RUNT_RELOAD = 80
RUNT_ODDS = 50
                
def StageOne(hero, winstyle = 0):
        
        # Initialize screen
        pygame.init()
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        pygame.display.set_caption('Cyborg-Fu!')

        # Creating Background
        bgdtile = load_image('graytile.png')
        background = pygame.Surface(SCREENRECT.size)
        for x in range(0, SCREENRECT.width, bgdtile.get_width()):
                for y in range(0, SCREENRECT.height, bgdtile.get_width()):
                        background.blit(bgdtile, (x, y))

        #Missle & Attack object groups must be determined before characters.
        shots = pygame.sprite.Group()
        pshots = pygame.sprite.Group()
        claws = pygame.sprite.Group()
        blade = pygame.sprite.Group()
        blood = pygame.sprite.Group()
        runties = pygame.sprite.Group()
        
        Runt([100, 100])
        prof = Creature("prof", [740, 30], [1, 1], [10], "still", "prof.png", "nil")

        #Scoreboard
        score = Score()
        scoresprite = pygame.sprite.RenderPlain(score)
                
        #Text
        TEXT = "Professor: Let's see what they can do..."
        text = Text(TEXT)
        textgroup = pygame.sprite.Group()

        #Create Characters
        global gunner
        global tesi
        if hero == "tesi":
                tesi = Tesi(blade)
                life = Life(tesi)
                lifesprite = pygame.sprite.RenderPlain(life)
                heroes = pygame.sprite.Group(tesi)
                sprites = pygame.sprite.Group(tesi, prof, score, life, text)
        if hero == "gunner":
                gunner = Hero(shots)
                life = Life(gunner)
                lifesprite = pygame.sprite.RenderPlain(life)
                heroes = pygame.sprite.Group(gunner)
                sprites = pygame.sprite.Group(gunner, prof, score, life, text)
                
        
        #Assign life values
        Alives = 0
        Blives = 0
        Clives = 0
        Dlives = 0
        Elives = 0
        
        #Checkmarks to avoid repeating text
        CHECKMARK1 = 0
        CHECKMARK2 = 0
        CHECKMARK3 = 0

        all = pygame.sprite.Group(prof, score, life, text, blood, pshots, blade, claws, runties, shots)
        
        #Default groups for each sprite class
        Creature.containers = all
        Shot.containers = all
        PowerShot.containers = all
        Runt.containers = all
        Text.containers = all

        
        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Initialise clock
        clock = pygame.time.Clock()

        #Tesi's blade
        BLADE = 1
        COLLIDELATENCY = 0
        runtreload = RUNT_RELOAD
        
        # Event loop
        while 1:
    
                clock.tick(60)

                COLLIDELATENCY = COLLIDELATENCY - 1

                """Creating actions that cause a change in dialogue"""
                if score.score == 4:
                        if CHECKMARK1 == 0:
                                msg = "Professor: Hmm, they seem to be working properly. Excellent!"
                                newText = Text(msg)
                                sprites.add(newText)
                                CHECKMARK1 = 1

                #I would very much like to get this code condensed, but it doesnt seem possible!
                if runtreload:
                        runtreload = runtreload - 1
                elif not int(random.random() * RUNT_ODDS):
                        choice = random.choice((1,2,3,4,5))
                        if choice == 1:
                                if Alives <= 0:
                                        runtA = Runt([100,50])
                                        runties.add(runtA)
                                        Alives = 1      
                        if choice == 2:
                                if Blives <= 0:
                                        runtB = Runt([200,50])
                                        runties.add(runtB)
                                        Blives = 1      
                        if choice == 3:
                                if Alives <= 0:
                                        runtC = Runt([300,50])
                                        runties.add(runtC)
                                        Clives = 1      
                        if choice == 4:
                                if Dlives <= 0:
                                        runtD = Runt([400,50])
                                        runties.add(runtD)
                                        Dlives = 1      
                        if choice == 5:
                                if Elives <= 0:
                                        runtE = Runt([500,50])
                                        runties.add(runtE)
                                        Elives = 1      
                        
                        runtreload = RUNT_RELOAD

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
                                        if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                                                tesi.state = "still"
                                        if event.key == K_e:
                                                tesi.healing = 0

                        # Tesi gets his blade back
                        if COLLIDELATENCY <= 0:
                                if pygame.sprite.spritecollide(tesi, blade, dokill):
                                        BLADE = BLADE + 1

                        if pygame.sprite.spritecollide(tesi, runties, dontkill):
                                tesi.bleed(blood)
                                tesi.life = tesi.life - 3

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
                    
                        if pygame.sprite.spritecollide(gunner, runties, dontkill):
                                gunner.bleed(blood)
                                gunner.life = gunner.life - 5
                                gunner.knockback()

               

                if Alives == 1:
                        if pygame.sprite.spritecollide(runtA, shots, dokill):
                                runtA.bleed(blood)
                                runtA.life = runtA.life - 10
                                if runtA.life <= 0:
                                        Alives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtA, pshots, dontkill):
                                runtA.bleed(blood)
                                runtA.life = runtA.life - 15
                                if runtA.life <= 0:
                                        Alives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtA, blade, dontkill):
                                runtA.bleed(blood)
                                runtA.life = runtA.life - 4
                                if runtA.life <= 0:
                                        Alives = 0
                                        score.plus(1)
                if Blives == 1:
                        if pygame.sprite.spritecollide(runtB, shots, dokill):
                                runtB.bleed(blood)
                                runtB.life = runtB.life - 10
                                if runtB.life <= 0:
                                        Blives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtB, pshots, dontkill):
                                runtB.bleed(blood)
                                runtB.life = runtB.life - 15
                                if runtB.life <= 0:
                                        Blives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtB, blade, dontkill):
                                runtB.bleed(blood)
                                runtB.life = runtB.life - 4
                                if runtB.life <= 0:
                                        Blives = 0
                                        score.plus(1)
                if Clives == 1:
                        if pygame.sprite.spritecollide(runtC, shots, dokill):
                                runtC.bleed(blood)
                                runtC.life = runtC.life - 10
                                if runtC.life <= 0:
                                        Clives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtC, pshots, dontkill):
                                runtC.bleed(blood)
                                runtC.life = runtC.life - 15
                                if runtC.life <= 0:
                                        Clives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtC, blade, dontkill):
                                runtC.bleed(blood)
                                runtC.life = runtC.life - 4
                                if runtC.life <= 0:
                                        Clives = 0
                                        score.plus(1)
                if Dlives == 1:
                        if pygame.sprite.spritecollide(runtD, shots, dokill):
                                runtD.bleed(blood)
                                runtD.life = runtD.life - 10
                                if runtD.life <= 0:
                                        Dlives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtD, pshots, dontkill):
                                runtD.bleed(blood)
                                runtD.life = runtD.life - 15
                                if runtD.life <= 0:
                                        Dlives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtD, blade, dontkill):
                                runtD.bleed(blood)
                                runtD.life = runtD.life - 4
                                if runtD.life <= 0:
                                        Dlives = 0
                                        score.plus(1)
                if Elives == 1:
                        if pygame.sprite.spritecollide(runtE, shots, dokill):
                                runtE.bleed(blood)
                                runtE.life = runtE.life - 10
                                if runtE.life <= 0:
                                        Elives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtE, pshots, dontkill):
                                runtE.bleed(blood)
                                runtE.life = runtE.life - 15
                                if runtE.life <= 0:
                                        Elives = 0
                                        score.plus(1)
                        if pygame.sprite.spritecollide(runtE, blade, dontkill):
                                runtE.bleed(blood)
                                runtE.life = runtE.life - 4
                                if runtE.life <= 0:
                                        Elives = 0
                                        score.plus(1)

                if pygame.sprite.spritecollide(prof, runties, dontkill):
                        msg = "Professor: (Sigh) Attack the subject, stupid runts!"
                        newText = Text(msg)
                        sprites.add(newText)
                        runties.empty()
                        Alives = 0
                        Blives = 0
                        Clives = 0
                        Dlives = 0
                        Elives = 0

                if pygame.sprite.spritecollide(prof, heroes, dontkill):
                        if score.score <= 9:
                                if CHECKMARK2 == 0:
                                        msg = "Professor: Attack the runts, let me see what you can do!"
                                        newText = Text(msg)
                                        sprites.add(newText)
                                        CHECKMARK2 = 1
                        if score.score >= 10:
                                if CHECKMARK3 == 0:
                                        msg = "I have finally succeeded. I shall call off these runts."
                                        newText = Text(msg)
                                        sprites.add(newText)
                                        CHECKMARK3 = 1
                                        runties.empty()
                                        Alives = 2
                                        Blives = 2
                                        Clives = 2
                                        Dlives = 2
                                        Elives = 2
                                        StageTwo(hero)
                                        
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

                textgroup.clear(screen, background)
                textgroup.update()
                textgroup.draw(screen)
                
                sprites.clear(screen, background)
                sprites.update()
                sprites.draw(screen)
                
                pygame.display.flip()

