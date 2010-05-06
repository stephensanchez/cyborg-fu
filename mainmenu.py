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
from pygame.locals import *
from StageOne import *
from DisplayObject import load_png

dokill = 1
dontkill = 0
SCREENRECT = Rect(0, 0, 800, 600)
SCORE = 0      #Score update
SHADOW_SPAWN = 20
SHADOW_ODDS = 20

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

        text = Text("Welcome, to Cyborg-Fu.  (Press the space bar to continue)", 20, 10)

        ARROW = "->"
        arrow = Text(ARROW, 20, 150)
        
        #Create Game Groups
        objects = pygame.sprite.Group(text)
        
        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()
        
        # Initialise clock
        clock = pygame.time.Clock()

        CHOICE = "sword"
        HERO = "tesi"

        choice = CHOICE
        hero = HERO

        messages = []
        messages.append(Text("You are a cyborg, programmed by me, the professor.", 20, 30))
        messages.append(Text("My work is complete, it is time to test you against some nasty little critters...", 20, 50))
        messages.append(Text("To move, use the W, A, S, and D keys.  Your basic attack can be used by the spacebar during battle.", 20, 70))
        messages.append(Text("For each stage I present you, try and gain twenty points, then come speak to me, I will advance you.", 20, 90))
        messages.append(Text("Press E through Y for possible special abilities, they will use your mana!", 20, 110))
        messages.append(Text("Which weapon do you prefer for battle?", 20, 130))

        # Event loop
        while 1:
            
                clock.tick(60)

                for event in pygame.event.get():
                        if event.type == QUIT: 
                                pygame.quit()
                                return
                       
                        if event.type == KEYDOWN:
                                if event.key == K_SPACE and len(messages) > 0:
                                        message = messages[0]
                                        objects.add(message)
                                        messages.remove(message)
                                if event.key == K_DOWN and len(messages) == 0:
                                        choice = "gun"
                                        arrow.locy = 170
                                if event.key == K_UP and len(messages) == 0:
                                        choice = "sword"
                                        arrow.locy = 150
                                if event.key == K_RETURN and len(messages) == 0:
                                        if choice == "sword":
                                                hero = "tesi"
                                        if choice == "gun":
                                                hero = "gunner"
                                        StageOne(hero)
                                                

                        if len(messages) == 0:
                                objects.add(Text("Sword", 50, 150))
                                objects.add(Text("Gun", 50, 170))
                                objects.add(Text("Use the up and down keys to select, then press enter.", 20, 190))
                                objects.add(arrow)
        
                objects.clear(screen, background)
                objects.update()
                objects.draw(screen)
                
                pygame.display.flip()

