import pygame
from DisplayObject import load_png

class Block(pygame.sprite.Sprite):

        """This is not a weapon but it is an object used by a player, and has
        a great deal of importance"""
        def __init__(self, position):
                pygame.sprite.Sprite.__init__(self)
                self.life = 100
                self.position = position
                self.image, self.rect = load_png('block.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.rect.midtop = self.position
                pygame.event.pump()

        def collision(self, sprite):
                sprite.movepos = [0,0]
                if sprite.facing == "left":
                        sprite.movepos = [1,0]
                if sprite.facing == "right":
                        sprite.movepos = [-1,0]
                if sprite.facing == "up":
                        sprite.movepos = [0,1]
                if sprite.facing == "down":
                        sprite.movepos = [0,-1]