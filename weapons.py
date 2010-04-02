#RPG Weapon Classes

try:
        import os
        import pygame
        import random
        from sprites import *

except ImportError, err:
        print "Module not found: %s" % (err)
        sys.exit(2)

#Why can't I use this in one script? Shouldn't have to copy so many times
def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
            image = pygame.image.load(fullname)
            if image.get_alpha() is None:
                    image = image.convert()
            else:
                    image = image.convert_alpha()
    except pygame.error, message:
             print 'Cannot load image:', fullname
    return image, image.get_rect()

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

class Pshot(Shot):
        """Gunner's Powershot, special skill"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 65
                self.state = "still"
                self.image, self.rect = load_png('powershot.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(position, facing)
        

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
                
                
class ThrownBlade(pygame.sprite.Sprite):
        """A scary (programming-wise) combination of the bullet and the blade"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 60
                self.position = position
                self.image, self.rect = load_png('blade.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.clock = 1
                self.state = "still"
                self.original = self.image
                self.reinit(position, facing)

        def reinit(self, position, facing):
                self.rect.midtop = self.position
                self.state = "moving"
                if facing == "right":
                        self.movepos = [6,0]
                elif facing == "left":
                        self.movepos = [-6,0]
                elif facing == "down":
                        self.movepos = [0,6]
                elif facing == "up":
                        self.movepos = [0,-6]

        def update(self):
                self.onWall()
                newpos = self.rect.move(self.movepos)
                if self.state == "still":
                        self.movepos = [0,0]
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()
                if self.state != "still":
                        self.spin(self.position)

        def spin(self, position):
                center = self.rect.center
                self.clock = self.clock + 30
                rotate = pygame.transform.rotate
                self.image = rotate(self.original, self.clock)
                self.rect = self.image.get_rect(center=center)
                if self.clock >= 1200 and self.clock <= 1201:
                        self.movepos[0] = -(self.movepos[0])
                        self.movepos[1] = -(self.movepos[1])
                elif self.clock >= 2400:
                        self.state = "still"

        def onWall(self):
                #Using +10 pixels due to bug in images...
                if self.rect.left < (self.area.left + 10) or \
                   self.rect.right > (self.area.right - 10) or \
                   self.rect.top < (self.area.top + 10) or \
                   self.rect.bottom > (self.area.bottom - 10):
                        self.state = "still"

class Club(pygame.sprite.Sprite):
        """Ogre's melee attack.  Oh, how brutal!"""
        def __init__(self, position, facing):
                pygame.sprite.Sprite.__init__(self)
                self.life = 10
                self.state = "still"
                self.clock = 0
                self.position = position
                self.image, self.rect = load_png('club.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit(self.position, facing)

        def reinit(self, position, facing):
                self.rect.midtop = self.position
                self.state = "moving"
                if facing == "right":
                        self.movepos = [35, 0]                                      
                elif facing == "left":
                        self.image = pygame.transform.rotate(self.image, 180)
                        self.movepos = [-40,0]
                elif facing == "down":
                        self.image = pygame.transform.rotate(self.image, 270)
                        self.movepos = [0,30]
                elif facing == "up":
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.movepos = [0,-50]
                newpos = self.rect.move(self.movepos)
                self.original = self.image
                if self.area.contains(newpos):
                        self.rect = newpos
                pygame.event.pump()

        def spin(self, position):
                center = self.rect.center
                self.clock = self.clock + 5
                rotate = pygame.transform.rotate
                self.image = rotate(self.original, self.clock)
                self.rect = self.image.get_rect(center=center)
    

        def update(self):
                self.spin(self.position)
                self.life = self.life - 1
                if self.life == 0:
                        self.kill()

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

class Block(pygame.sprite.Sprite):

        """This is not a weapon but it is an object used by a player, and has
        a great deal of importance"""
        def __init__(self, position):
                pygame.sprite.Sprite.__init__(self)
                self.life = 100
                self.position = position
                self.image, self.rect = load_png('block.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.rect.midtop = self.position
                pygame.event.pump()

        def collision(self, sprite):
                sprite.movepos = [0,0]
                if sprite.facing == "left":
                        sprite.movepos = [1,0]
                if sprite.facing == "right":
                        sprite.movepos = [-1,0]
                if sprite.facing == "up":
                        sprite.movepos = [0,1]
                if sprite.facing == "down":
                        sprite.movepos = [0,-1]
                
    
                
        



