import pygame
from Shot import Shot
from DisplayObject import load_png

class PowerShot(Shot):
        """Gunner's Powershot, special skill"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 65
                self.state = "still"
                self.image, self.rect = load_png('powershot.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(position, facing)