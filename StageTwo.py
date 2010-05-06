"""
Copyright (c) 2010 Stephen Sanchez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import pygame
import random
import os
from pygame.locals import *
from StageThree import *
from Ogre import Ogre
from Tesi import Tesi
from Hero import Hero
from Creature import Creature
from Shot import Shot
from PowerShot import PowerShot
from main import *


dokill = 1
dontkill = 0
SCREENRECT = Rect(0, 0, 800, 600)
OGRE_RELOAD = 80
OGRE_ODDS = 50

def StageTwo(hero, winstyle = 0):
        
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
        

        prof = Creature("prof", [740, 30], [1, 1], [10], "still", "prof.png", "nil")
        Ogre([100, 100], clubs)
        
        #Text
        TEXT = "Ogres may seem stupid, but they're a lot smarter than runts! Be careful!"
        text = Text(TEXT)
        textgroup = pygame.sprite.Group()
        
        
        #Create Characters
        global tesi
        global gunner
        if hero == "tesi":
                tesi = Tesi(blade)
                life = Life(tesi)
                Mana(tesi)
                lifesprite = pygame.sprite.RenderPlain(life)
                heroes = pygame.sprite.Group(tesi)
                sprites = pygame.sprite.Group(tesi, prof, score, life, text)
        if hero == "gunner":
                gunner = Hero(shots)
                life = Life(gunner)
                Mana(gunner)
                lifesprite = pygame.sprite.RenderPlain(life)
                heroes = pygame.sprite.Group(gunner)
                sprites = pygame.sprite.Group(gunner, prof, score, life, text)

        #Assign life values
        Alives = 0
        Blives = 0

        #Checkmarks to avoid repeating text
        CHECKMARK1 = 0
        CHECKMARK2 = 0
        CHECKMARK3 = 0
        
        #Default groups for each sprite class
        Creature.containers = sprites
        Shot.containers = shots
        PowerShot.containers = pshots
        Ogre.containers = ogres
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
                                msg = "These Ogres cost a lot, I hope you can handle more than two!"
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
                                        ogreA = Ogre(loc, clubs)
                                        ogres.add(ogreA)
                                        Alives = 1
                        if choice == 2: 
                                if Blives <= 0:
                                        loc = [200, 50]
                                        ogreB = Ogre(loc, clubs)
                                        ogres.add(ogreB)
                                        Blives = 1
                                        
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

                                                        if Alives == 1:
                                                                ogreA.dodge()
                                                        if Blives == 1:
                                                                ogreB.dodge()
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
                                                        ogreA.dodge()
                                                if Blives == 1:
                                                        ogreB.dodge()
                                                        
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
                            
                if Alives == 1:
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
                if Blives == 1:
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
                                        StageThree(hero)

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
