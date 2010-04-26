import pygame
from DisplayObject import load_png

class ThrownBlade(pygame.sprite.Sprite):
        """A scary (programming-wise) combination of the bullet and the blade"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 60
                self.position = position
                self.image, self.rect = load_png('blade.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.clock = 1
                self.state = "still"
                self.original = self.image
                self.reinit(position, facing)

        def reinit(self, position, facing):
                self.rect.midtop = self.position
                self.state = "moving"
                if facing == "right":
                        self.movepos = [6,0]
                elif facing == "left":
                        self.movepos = [-6,0]
                elif facing == "down":
                        self.movepos = [0,6]
                elif facing == "up":
                        self.movepos = [0,-6]

        def update(self):
                self.onWall()
                newpos = self.rect.move(self.movepos)
                if self.state == "still":
                        self.movepos = [0,0]
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()
                if self.state != "still":
                        self.spin(self.position)

        def spin(self, position):
                center = self.rect.center
                self.clock = self.clock + 30
                rotate = pygame.transform.rotate
                self.image = rotate(self.original, self.clock)
                self.rect = self.image.get_rect(center=center)
                if self.clock >= 1200 and self.clock <= 1201:
                        self.movepos[0] = -(self.movepos[0])
                        self.movepos[1] = -(self.movepos[1])
                elif self.clock >= 2400:
                        self.state = "still"

        def onWall(self):
                #Using +10 pixels due to bug in images...
                if self.rect.left < (self.area.left + 10) or \
                   self.rect.right > (self.area.right - 10) or \
                   self.rect.top < (self.area.top + 10) or \
                   self.rect.bottom > (self.area.bottom - 10):
                        self.state = "still"