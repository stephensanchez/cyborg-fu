import pygame
from DisplayObject import load_png
from Creature import Creature

class Assassin(Creature):
        """Tough Boss character that'll shoot down the hero"""
        def __init__(self, spawn, attack):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "assassin"
                self.speed = [1,1]
                self.life = 400
                self.state = "still"
                self.graphic = "assassin.png"
                self.counter = 50
                self.spawn = spawn
                self.shotcounter = 10
                self.attack = attack
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()