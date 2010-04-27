import pygame
from DisplayObject import load_png
from Creature import Creature

class Tesi(Creature):
        """Double Bladed Swordsman """
        def __init__(self, attack):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "tesi"
                self.speed = [3,3]
                self.life = 300
                self.state = "still"
                self.graphic = "tesi.png"
                self.counter = 100
                self.spawn = [650, 550]
                self.attack = attack
                #Determines whether the user is pulling the mana.
                self.pull = 0
                self.mana = 0
                self.healing = 0
                self.exp = 0
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()