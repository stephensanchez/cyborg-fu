#RPG objects
#Starting with a hero and a monster

try:
        import os
        import pygame
        import random
        from Blood import Blood
        from Club import Club
        from Blade import Blade
        from ThrownBlade import ThrownBlade
        from PowerShot import PowerShot
        from Gun import Gun
        from Shot import Shot
        from StageTwo import *
        
except ImportError, err:
        print "Module not found: %s" % (err)
        sys.exit(2)

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

class SuperSprite(pygame.sprite.Sprite):
        """This is the definition of all sprites,
        common traits for one and all"""
        def __init__(self, nature, spawn, speed, life, state, graphic, attack):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = nature
                self.speed = speed
                self.life = life
                self.state = state
                self.graphic = graphic
                self.attack = attack
                self.counter = 100
                self.spawn = spawn
                self.image, self.rect = load_png(graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()

        def reinit(self):
                self.state = "still"
                self.movepos = [0,0]
                firstpos = self.rect.move(self.spawn)
                if self.area.contains(firstpos):
                            self.rect = firstpos
                self.original = self.image

        def update(self):
                if self.nature == "runt" or self.nature == "assassin":
                        self.wanderer()
                if self.nature == "tesi":
                        self.heal()
                        self.regen()
                if self.nature == "gunner":
                        self.regen()
                self.offWall()
                if self.state == "still":
                        self.movepos = [0,0]
                else:
                        newpos = self.rect.move(self.movepos)
                        if self.area.contains(newpos):
                                self.rect = newpos
                pygame.event.pump()
                if self.life <= 0:
                        self.kill()

        def moveup(self):
                self.movepos[1] = self.movepos[1] - (self.speed[1])
                self.state = "moveup"
                self.turn("up")

        def movedown(self):
                self.movepos[1] = self.movepos[1] + (self.speed[1])
                self.state = "movedown"
                self.turn("down")

        def moveleft(self):
                self.movepos[0] = self.movepos[0] - (self.speed[0])
                self.state = "moveleft"
                self.turn("left")

        def moveright(self):
                self.movepos[0] = self.movepos[0] + (self.speed[0])
                self.state = "moveright"
                self.turn("right")

        def turn(self, facing):
                self.facing = facing
                if self.facing == "up":
                        self.image = pygame.transform.rotate(self.original, 0)
                if self.facing == "down":
                        self.image = pygame.transform.rotate(self.original, 180)
                if self.facing == "left":
                        self.image = pygame.transform.rotate(self.original, 90)
                if self.facing == "right":
                        self.image = pygame.transform.rotate(self.original, 270)

        """Rather important to show that a character has been hit and damaged"""
        def bleed(self, bloodgroup):
                newBlood = Blood(self.rect.center)
                bloodgroup.add(newBlood)
                
        def knockback(self):
                knock = [10,10]
                direction = self.facing
                self.state = "still"
                if direction == "up":
                        self.movepos[1] = self.movepos[1] - (knock[1])
                        self.rect = self.rect.move(self.movepos)
                if direction == "down":
                        self.movepos[1] = self.movepos[1] + (knock[1])
                        self.rect = self.rect.move(self.movepos)
                if direction == "left":
                        self.movepos[0] = self.movepos[0] - (knock[0])
                        self.rect = self.rect.move(self.movepos)
                if direction == "right":
                        self.movepos[0] = self.movepos[0] + (knock[0])
                        self.rect = self.rect.move(self.movepos)
                

                                                
        def offWall(self):
                #Using +10 pixels due to bug in images...
                if self.rect.left < (self.area.left + 10) or self.rect.right > (self.area.right - 10):
                        self.movepos[0] = -(self.movepos[0])
                elif self.rect.top < (self.area.top + 10) or self.rect.bottom > (self.area.bottom - 10):
                        self.movepos[1] = -(self.movepos[1])

        def aim(self, direction):
                #Definition of aiming for the hero and shooting!
                xdifference = direction[0] - self.rect[0]
                ydifference = direction[1] - self.rect[1]
                self.shotcounter = self.shotcounter - 1
                if self.shotcounter == 0:
                        self.shotcounter = 5
                        TURN_ODDS = 100
                        if int(random.random() * TURN_ODDS):
                                choice = random.choice((1,2,3))
                                if choice == 1:
                                        if xdifference < 30 and ydifference < 30 and ydifference > -30:
                                                self.moveleft()
                                                self.fire(self.attack)
                                        if xdifference > -30 and ydifference < 30 and ydifference > -30:
                                                self.moveright()
                                                self.fire(self.attack)
                                        if ydifference < 30 and xdifference < 30 and xdifference > -30:
                                                self.moveup()
                                                self.fire(self.attack)
                                        if ydifference > -30 and xdifference < 30 and xdifference > -30:
                                                self.movedown()
                                                self.fire(self.attack)
                
        def tryclub(self, direction):
                #Determines whether or not to swing the club.
                xdifference = direction[0] - self.rect[0]
                ydifference = direction[1] - self.rect[1]
                
                self.clubcounter = self.clubcounter - 1
                if self.clubcounter == 0:
                        self.clubcounter = 10
                        TURN_ODDS = 100
                        if int(random.random() * TURN_ODDS):
                                if xdifference < 65 and xdifference > -65 and ydifference < 65 and ydifference > -65:
                                        self.club(self.attack)
                                        
        """The Ogre Clubbing skill"""
        def club(self, clubgroup):
                self.state = "still"
                newClub = Club(self.rect.center, self.facing)
                clubgroup.add(newClub)

        """Follows the target hero, given by direction = hero.pos"""

        def chase(self, direction):
                #Chases hero
                xdifference = direction[0] - self.rect[0]
                ydifference = direction[1] - self.rect[1]
                
                self.counter = self.counter - 1
                if self.counter == 0:
                        self.counter = 10
                        TURN_ODDS = 100
                        if int(random.random() * TURN_ODDS):
                                self.movepos = [0,0]
                                if xdifference > 50:
                                        self.moveright()
                                if ydifference > 50:
                                        self.movedown()
                                if xdifference < -50:
                                        self.moveleft()
                                if ydifference < -50:
                                        self.moveup()


        """Randomly lets a monster jump slightly to avoid an attack"""

        def dodge(self):
                choice = random.choice((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))
                if choice == 1:
                        self.movepos = [0,2]
                if choice == 2:
                        self.movepos = [0,-2]
                if choice == 3:
                        self.movepos = [2,0]
                if choice == 4:
                        self.movepos = [-2,0]
                if choice == 5:
                        self.movepos = [2,2]
                if choice == 6:
                        self.movepos = [-4,4]
                if choice == 7:
                        self.movepos = [4,-4]
                if choice == 8:
                        self.movepos = [-4,-4]

        """Used for the runts' random roaming through the stages"""

        def wanderer(self):
                self.counter = self.counter - 1
                if self.counter == 0:
                        self.counter = 100
                        self.state = "still"
                        TURN_ODDS = 100
                        if int(random.random() * TURN_ODDS):
                                choice = random.choice((1,2,3,4,5))
                                self.movepos = [0,0]
                                if choice == 1:
                                       self.moveup()
                                if choice == 2:
                                        self.movedown()
                                if choice == 3:
                                        self.moveleft()
                                if choice == 4:
                                        self.moveright()
                                if choice == 5:
                                        self.state = "still"

        """These two classes define the two attacks created for Tesi, the sword
        slinging big-guy.  Who knows, though, they may be used for someone else"""

        def swing(self, bladegroup):
                self.state = "still"
                newBlade = Blade(self.rect.center, self.facing)
                bladegroup.add(newBlade)

        def throw(self, bladegroup):
                newThrownBlade = ThrownBlade(self.rect.midtop, self.facing)
                bladegroup.add(newThrownBlade)

        """These are classes designed for the Gunner.  They may eventually be used for
        new types of monsters.  The fire command is no longer used by the hero, not very effective or beneficial..."""

        def fire(self, shotgroup):
                newShot = Shot(self.rect.midtop, self.facing)
                shotgroup.add(newShot)

        def doublefire(self, shotgroup):
                if self.facing == "right" or self.facing == "left":
                        firstShot = Shot(self.rect.midtop, self.facing)
                        secondShot = Shot(self.rect.midbottom, self.facing)
                if self.facing == "up" or self.facing == "down":
                        firstShot = Shot(self.rect.midleft, self.facing)
                        secondShot = Shot(self.rect.midright, self.facing)
                shotgroup.add(firstShot)
                shotgroup.add(secondShot)

        """Here I will try to create some MANA abilities, such as a healing power.
        This will be an interesting aspect if I can get it to work."""

        def regen(self):
            maxmana = 300
            choice = random.choice((1,2,3,4,5))
            if choice == 1 and self.mana < maxmana:
                    self.mana = self.mana + 1
            
        def heal(self):
            maxlife = 300
            radius = 35
            screen = pygame.display.get_surface()
            pos = self.rect.center
            green = (0, 250, 0)
            blue = (0, 0, 250)
            color = random.choice((green, blue))
            width = 2
            if self.healing == 1:
                    if self.mana > 3 and self.life < maxlife:
                            self.state = "still"
                            self.mana = self.mana - 4
                            self.life = self.life + 1
                            pygame.draw.circle(screen, color, pos, radius, width)

        def powershot(self, shotgroup):
                if self.mana > 19:
                        self.mana = self.mana - 20
                        if self.facing == "right" or self.facing == "left":
                                firstShot = PowerShot(self.rect.midtop, self.facing)
                                secondShot = PowerShot(self.rect.midbottom, self.facing)
                        if self.facing == "up" or self.facing == "down":
                                firstShot = PowerShot(self.rect.midleft, self.facing)
                                secondShot = PowerShot(self.rect.midright, self.facing)
                        shotgroup.add(firstShot)
                        shotgroup.add(secondShot)
                            

class Runt(SuperSprite):
        """Blind wandering little green monster """
        def __init__(self, spawn):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "runt"
                self.speed = [1,1]
                self.life = 100
                self.state = "still"
                self.graphic = "runt.png"
                self.counter = 100
                self.spawn = spawn
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()

class Tesi(SuperSprite):
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

class Hero(SuperSprite):
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
                
class Ogre(SuperSprite):
        """Big slow strong ogre, should seek the player, and have an attack"""
        def __init__(self, spawn, attack):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "ogre"
                self.speed = [1,1]
                self.life = 500
                self.state = "still"
                self.graphic = "ogre.png"
                self.counter = 10
                self.clubcounter = 5
                self.attack = attack
                self.spawn = spawn
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()

class Assassin(SuperSprite):
        """Tough Boss character that'll shoot down the hero"""
        def __init__(self, spawn, attack):
                pygame.sprite.Sprite.__init__(self)
                self.facing = "right"
                self.nature = "assassin"
                self.speed = [1,1]
                self.life = 400
                self.state = "still"
                self.graphic = "assassin.png"
                self.counter = 50
                self.spawn = spawn
                self.shotcounter = 10
                self.attack = attack
                self.image, self.rect = load_png(self.graphic)
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.reinit()
                
class Shadow(SuperSprite):
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
