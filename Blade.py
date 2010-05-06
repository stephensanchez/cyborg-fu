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

class Blade(pygame.sprite.Sprite):
        """Tesi's Swinging Blade.  Spins above his head as melee attack"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 10
                self.state = "still"
                self.position = position
                self.image, self.rect = load_png('blade.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.original = self.image
                self.reinit(self.position, facing)

        def reinit(self, position, facing):
                self.rect.midtop = self.position
                self.state = "moving"
                if facing == "right":
                        self.movepos = [40, 0]
                elif facing == "left":
                        self.movepos = [-40,0]
                elif facing == "down":
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.movepos = [0,20]
                elif facing == "up":
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.movepos = [0,-70]
                newpos = self.rect.move(self.movepos)
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()

        def update(self):
                self.life = self.life - 1
                if self.life == 0:
                        self.kill()