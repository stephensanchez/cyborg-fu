"""
Copyright (c) 2010 Stephen Sanchez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
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