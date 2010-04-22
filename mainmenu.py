#!/usr/bin/env python
#The makings of my own Network RPG
#Many ideas come to mind but who knows how the game will play...

import pygame
import random
from pygame.locals import *
from StageOne import *

dokill = 1
dontkill = 0
SCREENRECT = Rect(0, 0, 800, 600)
SCORE = 0      #Score update
SHADOW_SPAWN = 20
SHADOW_ODDS = 20


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error())
    return surface.convert()

class Text(pygame.sprite.Sprite):
        def __init__(self, text, locx, locy):
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.Font(None, 20)
            self.text = text
            self.locx = locx
            self.locy = locy
            screen = pygame.display.get_surface()
            self.update()
            self.rect = self.image.get_rect().move(self.locx, self.locy)

        def update(self):
                self.image = self.font.render(self.text, 0, (0, 255, 0))
                self.rect = self.image.get_rect().move(self.locx, self.locy)

def next(checkmark, group):

        if checkmark == 1:
                msg = "You are a cyborg, programmed by me, the professor.You have been created to protect me from my enemies!"
                newText = Text(msg, 20, 50)
                group.add(newText)

        if checkmark == 2:
                msg = "My work is complete, it is time to test you against some nasty little critters..."
                newText = Text(msg, 20, 80)
                group.add(newText)

        if checkmark == 3:
                msg = "To move, use the W, A, S, and D keys.  Your basic attack can be used by the spacebar during battle."
                newText = Text(msg, 20, 120)
                group.add(newText)

        if checkmark == 4:
                msg = "For each stage I present you, try and gain twenty points, then come speak to me, I will advance you."
                newText = Text(msg, 20, 150)
                group.add(newText)

        if checkmark == 5:
                msg = "Press E through Y for possible special abilities, they will use your mana!"
                newText = Text(msg, 20, 180)
                group.add(newText)

        if checkmark == 6:
                msg = "Now, I shall test your free will!  Which weapon do you prefer for battle?"
                sword = "Sword"
                gun = "Gun"
                msg2 = "Use the up and down keys to select, then press enter."
                newText = Text(msg, 20, 210)
                swordText = Text(sword, 50, 250)
                gunText = Text(gun, 50, 280)
                msg2 = Text(msg2, 20, 310)
                group.add(newText)
                group.add(swordText)
                group.add(gunText)
                group.add(msg2)


def mainmenu(winstyle = 0):

        # Initialize screen
        pygame.init()
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        pygame.display.set_caption('Cyborg-Fu!')

        # Creating Background
        background = pygame.Surface(SCREENRECT.size)
        background = background.convert()
        background.fill((0, 0, 0))

         #Text
        TEXT = "Welcome, to Cyborg-Fu.  Press the space bar to continue..."
        text = Text(TEXT, 20, 20)

        ARROW = "->"
        arrow = Text(ARROW, 20, 250)
        
        #Create Game Groups
        objects = pygame.sprite.Group(text)
        
        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        #Checkmarks for dialogue
        CHECKMARK = 0
        
        # Initialise clock
        clock = pygame.time.Clock()

        CHOICE = "sword"
        HERO = "tesi"

        choice = CHOICE
        hero = HERO

        # Event loop
        while 1:
            
                clock.tick(60)

                for event in pygame.event.get():
                        if event.type == QUIT: 
                                pygame.quit()
                                return
                       
                        if event.type == KEYDOWN:
                                if event.key == K_SPACE:
                                        CHECKMARK = CHECKMARK + 1
                                        next(CHECKMARK, objects)
                                if event.key == K_DOWN and CHECKMARK > 4:
                                        choice = "gun"
                                        arrow.locy = 280
                                        print choice
                                if event.key == K_UP and CHECKMARK > 4:
                                        choice = "sword"
                                        arrow.locy = 250
                                        print choice
                                if event.key == K_RETURN and CHECKMARK > 4:
                                        if choice == "sword":
                                                hero = "tesi"
                                        if choice == "gun":
                                                hero = "gunner"
                                        StageOne(hero)
                                                

                        if CHECKMARK == 6:
                                objects.add(arrow)
        
                objects.clear(screen, background)
                objects.update()
                objects.draw(screen)
                
                pygame.display.flip()

