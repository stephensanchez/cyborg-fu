import pygame
import random
from DisplayObject import load_png

class Blood(pygame.sprite.Sprite):
        """No, its not a weapon, but it is a result of them."""
        def __init__(self, position):
                pygame.sprite.Sprite.__init__(self)
                self.life = 100
                self.position = position
                self.image, self.rect = load_png('red.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(self.position)

        def reinit(self, position):
                self.rect.midtop = self.position
                choice = random.choice((1,2,3,4,5,6,7,8))
                if choice == 1:
                        self.movepos = [3,0]
                if choice == 2:
                        self.movepos = [0,3]
                if choice == 3:
                        self.movepos = [3,3]
                if choice == 4:
                        self.movepos = [-3,-3]
                if choice == 5:
                        self.movepos = [-3,0]
                if choice == 6:
                        self.movepos = [0,-3]
                if choice == 7:
                        self.movepos = [3,-3]
                if choice == 8:
                        self.movepos = [-3,3]

                newpos = self.rect.move(self.movepos)
                pygame.event.pump()

        def update(self):
                self.life = self.life - 1
                if self.life == 0:
                        self.kill()