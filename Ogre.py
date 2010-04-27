import pygame
from DisplayObject import load_png
from Creature import Creature

class Ogre(Creature):
        """Big slow strong ogre, should seek the player, and have an attack"""
        def __init__(self, spawn, attack):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "ogre"
                self.speed = [1,1]
                self.life = 500
                self.state = "still"
                self.graphic = "ogre.png"
                self.counter = 10
                self.clubcounter = 5
                self.attack = attack
                self.spawn = spawn
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()