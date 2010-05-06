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
   A Shot. Typically from a gun. Could come from something else, if one were
   so inclined. 
"""
class Shot(pygame.sprite.Sprite):
        """This is the bullet from the hero"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 60
                self.state = "still"
                self.image, self.rect = load_png('bullet.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(position, facing)

        def reinit(self, position, facing):
                self.state = "still"
                self.rect.midtop = position
                if facing == "right":
                        self.movepos = [9,0]
                elif facing == "left":
                        self.movepos = [-9,0]
                elif facing == "down":
                        self.movepos = [0,9]
                elif facing == "up":
                        self.movepos = [0,-9]

        def update(self):
                self.onWall()
                self.life = self.life - 1
                newpos = self.rect.move(self.movepos)
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()
                if self.life == 0:
                         self.kill()

        def onWall(self):
                #Using +10 pixels due to bug in images...
                if self.rect.left < (self.area.left + 10) or \
                   self.rect.right > (self.area.right - 10) or \
                   self.rect.top < (self.area.top + 10) or \
                   self.rect.bottom > (self.area.bottom - 10):
                        self.kill()