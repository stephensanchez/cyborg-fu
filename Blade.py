import pygame
from DisplayObject import load_png

class Blade(pygame.sprite.Sprite):
        """Tesi's Swinging Blade.  Spins above his head as melee attack"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 10
                self.state = "still"
                self.position = position
                self.image, self.rect = load_png('blade.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.original = self.image
                self.reinit(self.position, facing)

        def reinit(self, position, facing):
                self.rect.midtop = self.position
                self.state = "moving"
                if facing == "right":
                        self.movepos = [40, 0]
                elif facing == "left":
                        self.movepos = [-40,0]
                elif facing == "down":
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.movepos = [0,20]
                elif facing == "up":
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.movepos = [0,-70]
                newpos = self.rect.move(self.movepos)
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()

        def update(self):
                self.life = self.life - 1
                if self.life == 0:
                        self.kill()