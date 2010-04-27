import pygame
from DisplayObject import load_png
from Creature import Creature

class Hero(Creature):
        """Cowboy-guy with a gun. Fancy shmancy (And my first hero. I'm proud) """
        def __init__(self, attack):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "gunner"
                self.speed = [3,3]
                self.life = 100
                self.state = "still"
                self.graphic = "hero.png"
                self.counter = 100
                self.spawn = [650, 550]
                self.attack = attack
                self.mana = 0
                #Keeps the score, in all hopes.
                self.exp = 0
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()