import pygame
from DisplayObject import load_png

"""
   The gun. Your standard point and shoot interface. 
"""
class Gun(pygame.sprite.Sprite):
        """The default class to creating a gun type weapon"""
        def __init__(self, char, facing):
                pygame.sprite.Sprite.__init__(self)
                self.state = "still"
                self.positioning = char
                self.image, self.rect = load_png('gun.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(facing)

        def reinit(self, facing):
                self.state = "still"
                self.movepos = [0, 0]
                self.rect.midtop = self.positioning
                self.loc(facing)

        def update(self):
                newpos = self.rect.move(self.movepos)
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()

        def loc(self, facing):
                if facing == "right":
                        self.rect.midtop = self.positioning
                elif facing == "left":
                        self.rect.midtop = self.positioning
                elif facing == "down":
                        self.rect.midtop = self.positioning
                elif facing == "up":
                        self.rect.midtop = self.positioning