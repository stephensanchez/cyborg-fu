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

"""
   The gun. Your standard point and shoot interface. 
"""
class Gun(pygame.sprite.Sprite):
        """The default class to creating a gun type weapon"""
        def __init__(self, char, facing):
                pygame.sprite.Sprite.__init__(self)
                self.state = "still"
                self.positioning = char
                self.image, self.rect = load_png('gun.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(facing)

        def reinit(self, facing):
                self.state = "still"
                self.movepos = [0, 0]
                self.rect.midtop = self.positioning
                self.loc(facing)

        def update(self):
                newpos = self.rect.move(self.movepos)
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()

        def loc(self, facing):
                if facing == "right":
                        self.rect.midtop = self.positioning
                elif facing == "left":
                        self.rect.midtop = self.positioning
                elif facing == "down":
                        self.rect.midtop = self.positioning
                elif facing == "up":
                        self.rect.midtop = self.positioning