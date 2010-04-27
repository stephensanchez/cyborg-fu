import pygame
from DisplayObject import load_png
from Creature import Creature

class Runt(Creature):
        """Blind wandering little green monster """
        def __init__(self, spawn):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "runt"
                self.speed = [1,1]
                self.life = 100
                self.state = "still"
                self.graphic = "runt.png"
                self.counter = 100
                self.spawn = spawn
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()