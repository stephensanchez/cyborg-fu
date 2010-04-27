import pygame
from Creature import Creature
from DisplayObject import load_png

class Shadow(Creature):
        """The assassin should spawn these to throw off the player"""
        def __init__(self, spawn, attack, facing, running):
                pygame.sprite.Sprite.__init__(self)
                self.facing = facing
                self.nature = "assassin"
                self.speed = [1,2]
                self.life = 1
                self.state = "whatever"
                #move with the assassin
                self.movepos = running
                self.graphic = "assassin.png"
                self.counter = 50
                self.spawn = spawn
                self.shotcounter = 50
                self.attack = attack
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()