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
import random
from DisplayObject import load_png

class Blood(pygame.sprite.Sprite):
        """No, its not a weapon, but it is a result of them."""
        def __init__(self, position):
                pygame.sprite.Sprite.__init__(self)
                self.life = 100
                self.position = position
                self.image, self.rect = load_png('red.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(self.position)

        def reinit(self, position):
                self.rect.midtop = self.position
                choice = random.choice((1,2,3,4,5,6,7,8))
                if choice == 1:
                        self.movepos = [3,0]
                if choice == 2:
                        self.movepos = [0,3]
                if choice == 3:
                        self.movepos = [3,3]
                if choice == 4:
                        self.movepos = [-3,-3]
                if choice == 5:
                        self.movepos = [-3,0]
                if choice == 6:
                        self.movepos = [0,-3]
                if choice == 7:
                        self.movepos = [3,-3]
                if choice == 8:
                        self.movepos = [-3,3]

                newpos = self.rect.move(self.movepos)
                pygame.event.pump()

        def update(self):
                self.life = self.life - 1
                if self.life == 0:
                        self.kill()