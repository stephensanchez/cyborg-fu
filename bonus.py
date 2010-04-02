#!/usr/bin/env python
#Cyborg-Fu
#Many ideas come to mind but who knows how the game will play...

import pygame
import random
from pygame.locals import *
import os
from sprites import *
from assassin import *
from main import *

dokill = 1
dontkill = 0
SCREENRECT = Rect(0, 0, 800, 600)
OGRE_RELOAD = 80
OGRE_ODDS = 50

def bonus(hero, winstyle = 0):
        
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
        clubs = pygame.sprite.Group()
        blade = pygame.sprite.Group()
        blood = pygame.sprite.Group()
        ogres = pygame.sprite.Group()

        #scoreboard
        score = Score()
        scoresprite = pygame.sprite.RenderPlain(score)
        

        prof = SuperSprite("prof", [740, 30], [1, 1], [10], "still", "prof.png", "nil")
        Ogre([100, 100], clubs)
        
        #Text
        TEXT = "Bordom ensues! All monsters at once!"
        text = Text(TEXT)
        textgroup = pygame.sprite.Group()
        
        
        #Create Characters
        global tesi
        global gunner
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

        Shadow([100,300], fakeshots, "left", [0,0])

        #Checkmarks to avoid repeating text
        CHECKMARK1 = 0
        CHECKMARK2 = 0
        CHECKMARK3 = 0
        
        #Default groups for each sprite class
        SuperSprite.containers = sprites
        Shot.containers = shots
        Pshot.containers = pshots
        Ogre.containers = ogres
        Runt.containers = ogres
        Assassin.containers = ogres
        Text.containers = sprites
        
        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Initialise clock
        clock = pygame.time.Clock()

        #Tesi's blade
        BLADE = 1
        COLLIDELATENCY = 0
        ogrereload = OGRE_RELOAD
        
        # Event loop
        while 1:
    
                clock.tick(60)

                COLLIDELATENCY = COLLIDELATENCY - 1
                
                """Creating actions that cause a change in dialogue"""
                if score.score == 4:
                        if CHECKMARK1 == 0:
                                msg = "However, I'm already in my pajamas."
                                newText = Text(msg)
                                sprites.add(newText)
                                CHECKMARK1 = 1
                
                if ogrereload:
                        ogrereload = ogrereload - 1
                elif not int(random.random() * OGRE_ODDS):
                        choice = random.choice((1,2,3,4,5))
                        if choice == 1:
                                if Alives <= 0:
                                        loc = [100, 50]
                                        ogreA = Runt(loc)
                                        ogres.add(ogreA)
                                        Alives = 1
                        if choice == 2: 
                                if Blives <= 0:
                                        loc = [200, 50]
                                        ogreB = Runt(loc)
                                        ogres.add(ogreB)
                                        Blives = 1

                        if choice == 3:
                                if Clives <= 0:
                                        loc = [300, 50]
                                        ogreC = Ogre(loc, clubs)
                                        ogres.add(ogreC)
                                        Clives = 1

                        if choice == 4:
                                if Dlives <= 0:
                                        loc = [400, 50]
                                        ogreD = Ogre(loc, clubs)
                                        ogres.add(ogreD)
                                        Dlives = 1

                        if choice == 5:
                                if Elives <= 0:
                                        loc = [500, 50]
                                        ogreE = Assassin(loc, ashots)
                                        ogres.add(ogreE)
                                        Elives = 1;
                                        
                        ogrereload = OGRE_RELOAD
                            
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

                                                        if Clives == 1:
                                                                ogreC.dodge()
                                                        if Dlives == 1:
                                                                ogreD.dodge()
                                                        if Elives == 1:
                                                                ogreE.dodge()
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

                        if pygame.sprite.spritecollide(tesi, clubs, dontkill):
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

                                                if Alives == 1:
                                                        ogreC.dodge()
                                                if Blives == 1:
                                                        ogreD.dodge()
                                                if Elives == 1:
                                                        ogreE.dodge()
                                                        
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


                        if pygame.sprite.spritecollide(gunner, clubs, dontkill):
                                gunner.bleed(blood)
                                gunner.life = gunner.life - 10
                                gunner.knockback()

                if hero == "tesi":
                            loc = tesi.rect
                if hero == "gunner":
                            loc = gunner.rect
                            
                if Clives == 1:
                        ogreA.chase(loc)
                        ogreA.tryclub(loc)
                        if pygame.sprite.spritecollide(ogreA, shots, dokill):
                                ogreA.bleed(blood)
                                ogreA.life = ogreA.life - 10
                                if ogreA.life <= 0:
                                        Alives = 0
                                        score.plus(2)
                        if pygame.sprite.spritecollide(ogreA, pshots, dontkill):
                                ogreA.bleed(blood)
                                ogreA.life = ogreA.life - 15
                                if ogreA.life <= 0:
                                        Alives = 0
                                        score.plus(2)
                        if pygame.sprite.spritecollide(ogreA, blade, dontkill):
                                ogreA.bleed(blood)
                                ogreA.life = ogreA.life - 4
                                if ogreA.life <= 0:
                                        Alives = 0
                                        score.plus(2)
                if Dlives == 1:
                        ogreB.chase(loc)
                        ogreB.tryclub(loc)
                        if pygame.sprite.spritecollide(ogreB, shots, dokill):
                                ogreB.bleed(blood)
                                ogreB.life = ogreB.life - 10
                                if ogreB.life <= 0:
                                        Blives = 0
                                        score.plus(2)
                        if pygame.sprite.spritecollide(ogreB, pshots, dontkill):
                                ogreB.bleed(blood)
                                ogreB.life = ogreB.life - 15
                                if ogreB.life <= 0:
                                        Blives = 0
                                        score.plus(2)
                        if pygame.sprite.spritecollide(ogreB, blade, dontkill):
                                ogreB.bleed(blood)
                                ogreB.life = ogreB.life - 4
                                if ogreB.life <= 0:
                                        Blives = 0
                                        score.plus(2)

                if pygame.sprite.spritecollide(prof, ogres, dontkill):
                        msg = "Professor: (Sigh) Attack the subject, stupid ogres!"
                        newText = Text(msg)
                        sprites.add(newText)
                        ogres.empty()
                        Alives = 0
                        Blives = 0

                if pygame.sprite.spritecollide(prof, heroes, dontkill):
                        if score.score <= 9:
                                if CHECKMARK2 == 0:
                                        msg = "Professor: Attack the ogres, let me see what you can do!"
                                        newText = Text(msg)
                                        sprites.add(newText)
                                        CHECKMARK2 = 1
                        if score.score >= 10:
                                if CHECKMARK3 == 0:
                                        msg = "Excellent work. What shall be your next challenge.. hm?"
                                        newText = Text(msg)
                                        sprites.add(newText)
                                        CHECKMARK3 = 1
                                        ogres.empty()
                                        Alives = 2
                                        Blives = 2
                                        assassin(hero)

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

                textgroup.clear(screen, background)
                textgroup.update()
                textgroup.draw(screen)
                
                sprites.clear(screen, background)
                sprites.update()
                sprites.draw(screen)
                
                pygame.display.flip()