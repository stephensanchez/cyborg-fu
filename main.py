#!/usr/bin/env python
#Main window screen.

from mainmenu import *
from DisplayObject import load_png
import os

def main():
        
        mainmenu()

if __name__ == '__main__': main()

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error())
    return surface.convert()

class Text(pygame.sprite.Sprite):
        def __init__(self, text):
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.Font(None, 20)
            self.text = text
            self.life = 300
            screen = pygame.display.get_surface()
            self.update()
            self.rect = self.image.get_rect().move(20, 20)

        def update(self):
                self.life = self.life - 1
                self.image = self.font.render(self.text, 0, (0, 0, 0))
                if self.life <= 0:
                        self.kill()

class Life(pygame.sprite.Sprite):
        def __init__(self, char):
                pygame.sprite.Sprite.__init__(self)
                self.char = char
                self.maxLife = char.life
                self.image, self.rect = load_png("health.png")
                self.update()
                self.rect = self.image.get_rect().move(50, 550)

        def update(self):
                screen = pygame.display.get_surface()
                xScale = float(self.char.life) / float(self.maxLife) * 300
                self.image = pygame.transform.scale(self.image, (int(xScale), 17))

class Mana(pygame.sprite.Sprite):
        def __init__(self, char):
                pygame.sprite.Sprite.__init__(self)
                self.char = char
                self.maxMana = 300
                self.image, self.rect = load_png("mana.png")
                self.rect = self.image.get_rect().move(50, 570)
                self.update()

        def update(self):
                screen = pygame.display.get_surface()
                xScale = (float(self.char.mana) / float(self.maxMana) * 300) + 1
                self.image = pygame.transform.scale(self.image, (int(xScale), 17))

class Score(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.score = 0
            self.font = pygame.font.Font(None, 20)
            self.lastscore = -1
            screen = pygame.display.get_surface()
            self.update()
            self.rect = self.image.get_rect().move(450, 550)

        def plus(self, int):
            self.score = self.score + int

        def update(self):
            if self.score != self.lastscore:
                self.lastscore = self.score
                msg = "Score:   %d         " % (self.score)
                self.image = self.font.render(msg, 0, (0, 0, 255))
