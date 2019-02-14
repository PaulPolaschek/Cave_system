"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: 
idea: clean python3/pygame template using pygame.math.vector2

"""
import pygame
#import math
import random
import os
import time
#import operator
import math
#import vectorclass2d as v
#import textscroller_vertical as ts
#import subprocess

"""Best game: 10 waves by Ines"""

def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 VectorSprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, pos.x pos.y, move.x, move.y
           by Leonard Michlmayr"""
        if sprite1.static and sprite2.static:
            return 
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        bdxs = sprite2.move.x - sx
        bdys = sprite2.move.y - sy
        cbdxs = sprite1.move.x - sx
        cbdys = sprite1.move.y - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            if not sprite2.static:
                sprite2.move.x -= 2 * dirx * dp
                sprite2.move.y -= 2 * diry * dp
            if not sprite1.static:
                sprite1.move.x -= 2 * dirx * cdp
                sprite1.move.y -= 2 * diry * cdp

class Flytext(pygame.sprite.Sprite):
    def __init__(self, x, y, text="hallo", color=(255, 0, 0),
                 dx=0, dy=-50, duration=2, acceleration_factor = 1.0, delay = 0, fontsize=22):
        """a text flying upward and for a short time and disappearing"""
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)  # THIS LINE IS IMPORTANT !!
        self.text = text
        self.r, self.g, self.b = color[0], color[1], color[2]
        self.dx = dx
        self.dy = dy
        self.x, self.y = x, y
        self.duration = duration  # duration of flight in seconds
        self.acc = acceleration_factor  # if < 1, Text moves slower. if > 1, text moves faster.
        self.image = make_text(self.text, (self.r, self.g, self.b), fontsize)  # font 22
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.time = 0 - delay

    def update(self, seconds):
        self.time += seconds
        if self.time < 0:
            self.rect.center = (-100,-100)
        else:
            self.y += self.dy * seconds
            self.x += self.dx * seconds
            self.dy *= self.acc  # slower and slower
            self.dx *= self.acc
            self.rect.center = (self.x, self.y)
            if self.time > self.duration:
                self.kill()      # remove Sprite from screen and from groups

class Mouse(pygame.sprite.Sprite):
    def __init__(self, radius = 50, color=(255,0,0), x=320, y=240,
                    startx=100,starty=100, control="mouse", ):
        """create a (black) surface and paint a blue Mouse on it"""
        self._layer=10
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.radius = radius
        self.color = color
        self.startx=startx
        self.starty=starty
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.delta = -10
        self.age = 0
        self.pos = pygame.mouse.get_pos()
        self.move = 0
        self.tail=[]
        self.create_image()
        self.rect = self.image.get_rect()
        self.control = control # "mouse" "keyboard1" "keyboard2"
        self.pushed = False

    def create_image(self):

        self.image = pygame.surface.Surface((self.radius*0.5, self.radius*0.5))
        delta1 = 12.5
        delta2 = 25
        w = self.radius*0.5 / 100.0
        h = self.radius*0.5 / 100.0
        # pointing down / up
        for y in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,0+y),(50*w,15*h+y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,15*h+y),(65*w,0+y),2)
    
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,100*h-y),(50*w,85*h-y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,85*h-y),(65*w,100*h-y),2)
        # pointing right / left                 
        for x in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (0+x,35*h),(15*w+x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (15*w+x,50*h),(0+x,65*h),2)
            
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (100*w-x,35*h),(85*w-x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (85*w-x,50*h),(100*w-x,65*h),2)
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self, seconds):
        if self.control == "mouse":
            self.x, self.y = pygame.mouse.get_pos()
        elif self.control == "keyboard1":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_w]:
                self.y -= delta
            if pressed[pygame.K_s]:
                self.y += delta
            if pressed[pygame.K_a]:
                self.x -= delta
            if pressed[pygame.K_d]:
                self.x += delta
        elif self.control == "keyboard2":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_UP]:
                self.y -= delta
            if pressed[pygame.K_DOWN]:
                self.y += delta
            if pressed[pygame.K_LEFT]:
                self.x -= delta
            if pressed[pygame.K_RIGHT]:
                self.x += delta
        elif self.control == "joystick1":
            pass
        elif self.control == "joystick2":
            pass
        if self.x < 0:
            self.x = 0
        elif self.x > Viewer.width:
            self.x = Viewer.width
        if self.y < 0:
            self.y = 0
        elif self.y > Viewer.height:
            self.y = Viewer.height
        self.tail.insert(0,(self.x,self.y))
        self.tail = self.tail[:128]
        self.rect.center = self.x, self.y
        self.r += self.delta   # self.r can take the values from 255 to 101
        if self.r < 151:
            self.r = 151
            self.delta = 10
        if self.r > 255:
            self.r = 255
            self.delta = -10
        self.create_image()

class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprit
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        #print(self.number, VectorSprite.numbers)
        self.create_image()
        #self.rect = self.image.get_rect()
        
        self.distance_traveled = 0 # in pixel
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)

    def _overwrite_parameters(self):
        """change parameters before create_image is called""" 
        pass

    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
            #self.color = None
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.bossnumber not in VectorSprite.numbers:
                if self.kill_with_boss:
                    self.kill()
            elif self.sticky_with_boss:
                #print("i am sticky", self.number, self.bossnumber)
                boss = VectorSprite.numbers[self.bossnumber]
                #self.pos = v.Vec2d(boss.pos.x, boss.pos.y)
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
        self.pos += self.move * seconds
        self.distance_traveled += self.move.length() * seconds
        self.age += seconds
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )

    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = Viewer.width 
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -Viewer.height
        # -------- right edge -----                
        if self.pos.x  > Viewer.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = Viewer.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   < -Viewer.height:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -Viewer.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0


class Spark(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((10,3))
        pygame.draw.line(self.image, self.color, (1,1),(random.randint(5,10),1), random.randint(1,3))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
    

class Explosion():
    
    def __init__(self, pos, red = 100, blue = 0, green = 0, dred = 5, dblue = 5,
                 dgreen = 5, minsparks=1, maxsparks=200, a1 = 0, a2 =360, max_age = 1):
        
        for _ in range(minsparks,maxsparks):
            a = random.randint(int(a1),int(a2))
            v = pygame.math.Vector2(random.randint(50,250),0)
            v.rotate_ip(a)
            self.pos = pygame.math.Vector2(pos.x, pos.y)
            self.max_age = max_age
            c= [ red + random.randint(-dred, dred), 
                      green + random.randint(-dgreen, dgreen),
                      blue + random.randint(-dblue, dblue)]
            for farbe in [0 ,1, 2]:
                if c[farbe]<0:
                    c[farbe] = 0
                if c[farbe] > 255:
                    c[farbe] = 255
            Spark(pos = self.pos, max_age = self.max_age, move = v, angle = a, color = c)
            

class Cannon(VectorSprite):
    
    def _overwrite_parameters(self):
        self.sticky_with_boss = True
        self.kill_with_boss = True
        #print("cannon:",self.bossnumber)
        self._layer = 9
        #print("ich bin kanone. meine bossnumber:", self.bossnumber)
        #print("meine eigene nummer", self.number)
        #print("meine boss position", VectorSprite.numbers[self.bossnumber].pos)
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.line(self.image, (100, 0, 0), (25,25), (50,25),5)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        rightvector = pygame.math.Vector2(1,0)
        mousevector = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                       -pygame.mouse.get_pos()[1])
        diffvector = mousevector - self.pos                               
        angle = rightvector.angle_to(diffvector)
        self.set_angle(angle)
        

class Player(VectorSprite):
    
    def _overwrite_parameters(self):
        self.rotdelta = 1
        self.rot = 255
        self.mass = 400
        self.radius = 25
        #print("i am the Player, ", self.number)
        #print("Player.number:", self.number)
        #Cannon(bossnumber = self.number, sticky_with_boss = True)
        #print(sebossnumber)
       
    def fire(self, angle):
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        a = angle
        t = pygame.math.Vector2(25, 0)
        t.rotate_ip(angle)
        total =  Game.shooting_angle * 2
        a1 = total / (Game.rockets + 1)
        b = a - Game.shooting_angle
        for i in range(Game.rockets):
                b += a1
                v = pygame.math.Vector2(100,0)
                v.rotate_ip(b)
                v += self.move
                Rocket(pos=p+t, move = v, angle = b, max_distance = Game.rocket_range)
       
    def move_forward(self):
        v = pygame.math.Vector2(Game.playerspeed,0)
        v.rotate_ip(self.angle)
        self.move += v
        Flame(bossnumber=self.number, pos = self.pos)
        if random.random() < 0.2:
            Smoke(pos = self.pos, gravity = None, max_age=3.0)
            5
        
    
    def create_image(self):
        self.image = pygame.Surface((20,20))
        pygame.draw.polygon(self.image, (255, 255, 0), ((0,0),(20,10),(0,20),(10,10)))
        #pygame.draw.line(self.image, (self.rot, 0, 0), (25,25), (50,25),5)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        self.rot += self.rotdelta
        if self.rot > 255:
            self.rot = 255
            self.rotdelta *= -1
        if self.rot < 1:
            self.rot = 1
            self.rotdelta *= -1
       
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        oldcenter = self.rect.center
        self.create_image() 
        self.rect.center = oldcenter
        self.set_angle(self.angle)

        
class Tile(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 3 # so that player will be over Tile, not below it
    
    
    def create_image(self):
        self.image = pygame.Surface((20,20))
        self.image.fill(self.color)
        pygame.draw.rect(self.image, (250,250,250), (0,0,20,20), 1)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
        
class EvilLaser(VectorSprite):
    
    def _overwrite_parameters(self):
        self.kill_on_edge = True
    
    def create_image(self):
        self.image = pygame.Surface((30,5))
        self.farbe = (random.randint(30,50),random.randint(200,255),random.randint(0,20))
        self.image.fill(self.farbe)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        

class EvilMonster(VectorSprite):
    
    def _overwrite_parameters(self):
        #self.rotdelta = 1
        self.rot = random.randint(5,250)
        self.rotdelta = random.randint(1,5) * random.choice((-1,1))
        self.radius = 25
        self.mass = random.randint(50, 150)
        self.hitpoints = 100
        
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, (255, 255, 0), (25,25), 25)
        pygame.draw.circle(self.image, (self.rot, 0, 0), (10,10), 10)
        pygame.draw.circle(self.image, (self.rot, 0, 0), (40,10), 10)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        self.rot += self.rotdelta
        if self.rot > 255:
            self.rot = 255
            self.rotdelta *= -1
        if self.rot < 1:
            self.rot = 1
            self.rotdelta *= -1
       
    def update(self, seconds):
        #---ai----
        if random.random() < 0.01:
            v = pygame.math.Vector2(1,0)
            v.rotate_ip(random.randint(0,360))
            v *= random.random()*50
            self.move = v
        VectorSprite.update(self, seconds)
        oldcenter = self.rect.center
        self.create_image() 
        self.rect.center = oldcenter
        self.set_angle(self.angle)
        if random.random() < 0.002:
            self.fire()
            
    def fire(self):
        # wir wissen, player1 hat number 0
        # gibts ihn noch?
        if 0 not in VectorSprite.numbers:
            return 
        p1 = VectorSprite.numbers[0]
        rightvector = pygame.math.Vector2(1,0)
        diffvector = p1.pos - self.pos
        diffvector.normalize_ip()
        a = rightvector.angle_to(diffvector)
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        EvilLaser(pos = p, angle=a, move=diffvector*50, max_age = 5)
        
    def kill(self):
        Explosion(pos = self.pos, red = 255, dred = 20, green = 255, dgreen = 20, blue = 0, a1 = 0, a2 = 360)
        Game.gold += 1
        VectorSprite.kill(self)
       
class Flame(VectorSprite):
    
    def _overwrite_parameters(self):
        self.sticky_with_boss = True
        self.max_age = 0.01
        
    
    def create_image(self):
        self.image = pygame.Surface((60,10))
        farbe1 = (random.randint(200,255),random.randint(0,50),random.randint(0,50))
        farbe2 = (random.randint(200,255),random.randint(10,66),random.randint(0,50))
        farbe3 = (random.randint(200,255),random.randint(100,166),random.randint(0,50)) 
        # größte Raute
        pygame.draw.polygon(self.image, farbe1, [ (30,5), (35, 0), (60,5), (35,10) ])
        # mittlere Raute
        pygame.draw.polygon(self.image, farbe2, [ (32,5), (36, 2), (55,5), (36,8) ])
        # kleinste Raute
        pygame.draw.polygon(self.image, farbe3, [ (35,5), (38, 3), (50,5), (38,7) ])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        self.set_angle(VectorSprite.numbers[self.bossnumber].angle-180)

class Smoke(VectorSprite):
    
    def _overwrite_parameters(self):
        self.pos = pygame.math.Vector2(self.pos.x, self.pos.y)
        #print("hallo ich bin ein smoke", self.pos)

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, self.color, (25,25),
                           3+int(self.age*3))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        self.create_image()
        self.rect=self.image.get_rect()
        self.rect.center=(self.pos.x, -self.pos.y)
        c = int(self.age * 100)
        c = min(255,c)
        self.color=(c,c,c)



class Rocket(VectorSprite):

    #def __init__(self, **kwargs):
    #    self.readyToLaunchTime = 0
    #    VectorSprite.__init__(self, **kwargs)
        
        
        #self.create_image()

    def _overwrite_parameters(self):
        self._layer = 1   
        self.kill_on_edge=True
        self.radius = 3
        self.mass = 20
        self.damage = 10
        self.color = (255,156,0)
        self.speed = Game.rocketspeed



    def create_image(self):
        self.image = pygame.Surface((10,5))
        pygame.draw.polygon(self.image, (255, 255, 0),
            [(0,0),(7,0),(10,2),(10,3),(7,4),(0,4)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
  #  def update(self, seconds):
        # --- speed limit ---
   #     if self.move.length() != self.speed:
     #       if self.move.length() < 0:
    #            self.move = self.move.normalize() * self.speed
    #        else:
    #            pass
    #    if self.move.length() > 0:
    #        self.set_angle(-self.move.angle_to(pygame.math.Vector2(-1,0)))
    #        self.move = self.move.normalize() * self.speed
    #        # --- Smoke ---
    #        if random.random() < 0.2 and self.age > 0.1:
    #            Smoke(pos=pygame.math.Vector2(self.pos.x, self.pos.y), 
    #               gravity=pygame.math.Vector2(0,4), max_age = 4)
    #    self.oldage = self.age
    #    VectorSprite.update(self, seconds)
    #    # new rockets are stored offscreen 500 pixel below Viewer.height
    #    if self.age > self.readyToLaunchTime and self.oldage < self.readyToLaunchTime:
    #        self.pos.y -= 500

#    def kill(self):
#        Explosion(pos=pygame.math.Vector2(self.pos.x, self.pos.y),max_age=2.1, color=(200,255,255), damage = self.damage)
#        VectorSprite.kill(self)    


class Game():
    
    menupoints = ["exit","hitpoints","speed","rockets","rocketspeed","increase shootingangle","decrease shootingangle"]
    rockets = 1
    playerhitpoints = 100
    playerspeed = 1
    rocketspeed = 1
    shooting_angle = 20
    gold = 0
    price = 10
    rocket_range = 200
    

class Viewer():
    width = 0
    height = 0
    def movement_indicator(self,vehicle,pygamepos, color=(0,200,0)):
        #----heading indicator
        pygame.draw.circle(self.screen,color,pygamepos,100,1)
        h=pygame.math.Vector2(100,0)
        h.rotate_ip(-vehicle.angle)
        target=pygamepos+h
        target=(int(target.x),int(target.y))
        pygame.draw.circle(self.screen,(0,128,0),target,3)           
       
        if vehicle.move.x ==0 and vehicle.move.y==0:
            return
        length=int(vehicle.move.length()/10)
        length=min(10,length)
        v=pygame.math.Vector2(100,0)
        v.rotate_ip(vehicle.move.angle_to(v))
        target=pygamepos+v
        pygame.draw.line(self.screen, color, pygamepos,target,length)


    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        Viewer.width = width    # make global readable
        Viewer.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((250,100,180)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        # ------ background images ------
        self.backgroundfilenames = [] # every .jpg file in folder 'data'
        try:
            for root, dirs, files in os.walk("data"):
                for file in files:
                    if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
                        self.backgroundfilenames.append(file)
            random.shuffle(self.backgroundfilenames) # remix sort order
        except:
            print("no folder 'data' or no jpg files in it")
        Viewer.bombchance = 0.015
        Viewer.rocketchance = 0.001
        Viewer.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.prepare_sprites()
        self.loadbackground()

    def loadbackground(self):
        
        try:
            self.background = pygame.image.load(os.path.join("data",
                 self.backgroundfilenames[Viewer.wave %
                 len(self.backgroundfilenames)]))
        except:
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((250, 100, 180)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (Viewer.width,Viewer.height))
        self.background.convert()
        
        
    def round_hole(self, mx, my, r=5):
        """fills a circle-shaped hole with '.' into self.lines,
           center is (mx,my) radius is r
        """
        for y in range(my-r, my+r):
            for x in range(mx-r, mx+r):
                distance = ( (mx-x)**2 + (my-y)**2 ) ** 0.5
                if round(distance,0) < r:
                    self.lines[y][x] = "."

               
    def rectangle_hole(self, x, y, xlength, ylength):
        """fills a rectangle-shaped hole with '.' into self.lines,
           upper left corner is x,y"""
        x -= xlength
        y -= ylength
        for y2 in range(y,y+ylength):
            for x2 in range(x,x+xlength):
                self.lines[y2][x2] = "."
        
            
    def generate_level(self, xtiles, ytiles):
        self.lines = []
        for y in range(ytiles):
            line = []
            for x in range(xtiles):
                line.append("B")
            self.lines.append(line)
        #print(self.lines) # level is in self.lines
        
        for _ in range(15):
            self.rectangle_hole(random.randint(0, len(line)), random.randint(0, len(self.lines)), random.randint(5,10), random.randint(5,10))
        
        for _ in range(15):
            self.round_hole(random.randint(5, len(line)-5), random.randint(5, len(self.lines)-5), random.randint(2,5))
        
        #self.round_hole(40,9, 8)
        
                
        
    def paint_level(self):
          for y, line in enumerate(self.lines):
              for x, char in enumerate(line):
                  p = pygame.math.Vector2(x*20 + 10, -y*20 - 30)
                  if char == "B":
                      Tile(pos=p, color=(100,100,100))
          #for x in range(10, Viewer.width, 20):
          #  for y in range(30, Viewer.height, 20):
          #      Tile(pos=pygame.math.Vector2(x, -y), color=(16,16,16))
   
        

    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.mousegroup = pygame.sprite.Group()
        self.monstergroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.lasergroup = pygame.sprite.Group()
        self.flytextgroup = pygame.sprite.Group()
        self.tilegroup = pygame.sprite.Group()

        Mouse.groups = self.allgroup, self.mousegroup
        EvilMonster.groups = self.allgroup, self.monstergroup
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        Player.groups = self.allgroup, self.playergroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Spark.groups = self.allgroup
        Smoke.groups = self.allgroup
        Flame.groups = self.allgroup
        EvilLaser.groups = self.allgroup, self.lasergroup
        Tile.groups = self.allgroup, self.tilegroup

   
        # ------ player1,2,3: mouse, keyboard, joystick ---
        self.player1 =  Player(warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2,-Viewer.height/2))
        self.cannon1 = Cannon(bossnumber=self.player1.number)
        
        self.mouse1 = Mouse(control="mouse", color=(255,0,0))
        self.mouse2 = Mouse(control='keyboard1', color=(255,255,0))
        self.mouse3 = Mouse(control="keyboard2", color=(255,0,255))
        self.mouse4 = Mouse(control="joystick1", color=(255,128,255))
        self.mouse5 = Mouse(control="joystick2", color=(255,255,255))

        xtiles = (Viewer.width-10) // 20
        ytiles = (Viewer.height-30) // 20
        self.generate_level(xtiles, ytiles)
        self.paint_level()
        
        #for x in range(20):
        #    EvilMonster(bounce_on_edge=True)
      
    def calculate_price(self, cursor):
        text = Game.menupoints[cursor]
        if text == "exit":
            Game.price = 0
        elif text == "rockets":
            Game.price = 1
        elif text == "hitpoints":
            Game.price = 15
        elif text == "speed":
            Game.price = 5
        elif text == "rocketspeed":
            Game.price = 5
   
    def menu(self):
        running = True
        cursor = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_m:
                        return
                    if event.key == pygame.K_DOWN:
                        cursor += 1
                        cursor = min(len(Game.menupoints)-1, cursor)
                        self.calculate_price(cursor)
                    if event.key == pygame.K_UP:
                        cursor -= 1
                        cursor = max(0, cursor)
                        self.calculate_price(cursor) 
                        #running = False
                    if event.key == pygame.K_RETURN:
                        #Flytext(500, 500, text=Game.menupoints[cursor])
                        text = Game.menupoints[cursor]
                        if text == "exit":
                            return
                        elif text == "rockets":
                            if Game.gold < Game.price:
                                Flytext(500, 500, text = "you need {} gold".format(Game.price))
                                break
                            Game.gold -= Game.price
                            Game.rockets += 1
                            t = "Rockets now: {}".format(Game.rockets)
                            Flytext(500, 500, text=t)
                        elif text == "hitpoints":
                            if Game.gold < Game.price:
                                Flytext(500, 500, text = "you need {} gold".format(Game.price))
                                break
                            Game.playerhitpoints += 1
                            t = "Playerhitpoints now: {}".format(Game.playerhitpoints)
                            Flytext(500, 500, text=t)
                        elif text == "speed":
                            if Game.gold < Game.price:
                                Flytext(500, 500, text = "you need {} gold".format(Game.price))
                                break
                            Game.playerspeed += 1
                            t = "Playerspeed now: {}".format(Game.playerspeed)
                            Flytext(500, 500, text=t)
                        elif text == "rocketspeed":
                            if Game.gold < Game.price:
                                Flytext(500, 500, text = "you need {} gold".format(Game.price))
                                break
                            Game.rocketspeed += 1
                            t = "Rocketspeed now: {}".format(Game.rocketspeed)
                            Flytext(500, 500, text=t)
                        elif text == "increase shootingangle":
                            if Game.shooting_angle >= 180:
                                Game.shooting_angle = 180
                            else:
                                Game.shooting_angle += 5
                                t = "shootingangle now: {}".format(Game.shooting_angle)
                                Flytext(500, 500, text = t)
                        elif text == "decrease shootingangle":
                            if Game.shooting_angle <= 0:
                                Game.shooting_angle = 0
                            else:
                                Game.shooting_angle -= 5
                                t = "shootingangle now: {}".format(Game.shooting_angle)
                                Flytext(500, 500, text = t)
                            
                        
            
            # ----- celar all ----
            self.screen.blit(self.background, (0, 0))
            seconds = self.clock.tick(self.fps) / 1000
            self.flytextgroup.update(seconds)
            self.flytextgroup.draw(self.screen)
            # draw status
            write(self.screen, "gold: {} price: {} rockets: {} shootingangle: {} playerspeed: {} FPS: {:8.3}".format(
            Game.gold, Game.price, Game.rockets, Game.shooting_angle, Game.playerspeed, self.clock.get_fps() ), x=10, y=10)
            
            #---- draw shootingangle
            
            # ellipse arc angle in Radiants
            start = (90 - Game.shooting_angle) * math.pi / 180
            end =   (90 + Game.shooting_angle) * math.pi / 180
            #print(start, end)
            # shema of ship
            pygame.draw.polygon(self.screen, (0,0,255), 
                     [(700, 300), (600, 600),(700, 550), (800, 600)], 3)
            # bogerl
            pygame.draw.arc(self.screen, ( 200,200,200), (600,200,200, 200), start, end, 2) 
            # radien
            middlevec = pygame.math.Vector2( 700, -300)
            w = pygame.math.Vector2(120, 0)
            w.rotate_ip(90 +Game.shooting_angle)
            v = middlevec + w
            pygame.draw.line(self.screen, ( 200,200, 200), (700,300), (v.x, -v.y))
            w = pygame.math.Vector2(120, 0)
            w.rotate_ip(90- Game.shooting_angle)
            v = middlevec + w
            pygame.draw.line(self.screen, ( 200,200, 200), (700,300), (v.x, -v.y))
            
            
            self.allgroup.update(seconds)
            

            # draw menu
            for a, line in enumerate(Game.menupoints):
                write(self.screen, line, x=200, y= 100+a*25)
            c = random.randint(64, 128)   #, random.randint(0,255), random.randint(0,255))
            write(self.screen, "--->", x = 120, y = 100+cursor * 25, color = (c,c,c))
            pygame.display.flip()
        # --- menu fertig -----
   
    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        self.dicke = 10
        self.dickedelta = 0.4
        self.rot = 255
        self.rotdelta = 5
        self.menutime = False
        self.menudeltatime = 0
        while running:
            milliseconds = self.clock.tick(self.fps) #
            if self.menutime:
                self.menudeltatime += milliseconds / 1000
                self.menutime = False
                seconds = milliseconds / 1000 - self.menudeltatime
                self.menudeltatime = 0
            else:
                seconds = milliseconds / 1000
            self.playtime += seconds
            
            if gameOver:
                if self.playtime > exittime:
                    break
            #Game over?
            #if not gameOver:
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_TAB:
                        self.player1.fire(self.cannon1.angle)
                    if event.key == pygame.K_m:
                        self.menutime = True
                        self.menu()
                    if event.key == pygame.K_e:
                        ep = pygame.math.Vector2(self.player1.pos.x, self.player1.pos.y)
                        Explosion(pos = ep, red = 100, dred = 20, minsparks = 200, maxsparks = 300)
                    # ---- -simple movement for self.player1 -------
                    if event.key == pygame.K_RIGHT:
                        self.player1.move += pygame.math.Vector2(10,0)
                    if event.key == pygame.K_LEFT:
                        self.player1.move += pygame.math.Vector2(-10,0)
                    if event.key == pygame.K_UP:
                        self.player1.move += pygame.math.Vector2(0,10)
                    if event.key == pygame.K_DOWN:
                        self.player1.move += pygame.math.Vector2(0,-10)
                    # ---- stop movement for self.player1 -----
                    if event.key == pygame.K_r:
                        self.player1.move *= 0.1 # remove 90% of movement
                    if event.key == pygame.K_b:
                        Game.playerspeed = 1
                        self.player1.move = pygame.math.Vector2(0,0)
                    
   
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            
            # ------ move indicator for self.player1 -----
            
            
            # --- line from eck to mouse ---
            
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            

            # if pressed_keys[pygame.K_LSHIFT]:
                # paint range circles for cannons
            if pressed_keys[pygame.K_a]:
                self.player1.rotate(3)
            if pressed_keys[pygame.K_d]:
                self.player1.rotate(-3)
            if pressed_keys[pygame.K_w]:
                self.player1.move_forward()
            if pressed_keys[pygame.K_s]:
                v = pygame.math.Vector2(1,0)
                v.rotate_ip(self.player1.angle)
                self.player1.move += -v
    
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            if left:
                self.player1.fire(angle = self.cannon1.angle)
                #if oldleft and not left:
            if right:
                self.player1.move_forward()
            
            oldleft, oldmiddle, oldright = left, middle, right

          
            
            # write text below sprites
            write(self.screen, "FPS: {:8.3}  rockets: {} gold: {}".format(
                self.clock.get_fps(), Game.rockets, Game.gold ), x=10, y=10)
            self.allgroup.update(seconds)

            # --------- collision detection between player and monster -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.monstergroup,
                             False, pygame.sprite.collide_mask)
                for m in crashgroup:
                    elastic_collision(p, m)
            
            # --------- collision detection between monster and other monsters -----                    
            for m in self.monstergroup:
                crashgroup = pygame.sprite.spritecollide(m, self.monstergroup,
                             False, pygame.sprite.collide_circle)
                for m2 in crashgroup:
                    if m.number != m2.number:
                        elastic_collision(m, m2)

            # --------- collision detection between monster and rockets -----                    
            for m in self.monstergroup:
                crashgroup = pygame.sprite.spritecollide(m, self.rocketgroup,
                             False, pygame.sprite.collide_circle)
                for r in crashgroup:
                    elastic_collision(m, r)
                    m.hitpoints -= r.damage
                    # winkel zwischen monstermittelpunkt und rocket
                    rightvector = pygame.math.Vector2(1,0)
                    diffvector = r.pos - m.pos
                    a = rightvector.angle_to(diffvector)
                    Explosion(pos = r.pos, red = 200, dred = 20, minsparks = 100, maxsparks = 200, a1 = a-40, a2 = a+40, max_age = 0.25)
                    r.kill()
                    
            # --------- collision detection between player and laser -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.lasergroup,
                             False, pygame.sprite.collide_mask)
                
                for l in crashgroup:
                    #elastic_collision(p,l)
                    p.hitpoints -= l.damage 
                    rightvector = pygame.math.Vector2(1,0)
                    diffvector = l.pos - p.pos
                    a = rightvector.angle_to(diffvector)
                    Explosion(pos = l.pos, red = 0, dred = 0, blue = 0, dblue = 0, green = 200, dgreen = 20, minsparks = 100, maxsparks = 200, a1 = a-40, a2 = a+40, max_age = 0.25)
                    l.kill()
            
            
            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)
            
            # --- Martins verbesserter Mousetail -----
            for mouse in self.mousegroup:
                if len(mouse.tail)>2:
                    for a in range(1,len(mouse.tail)):
                        r,g,b = mouse.color
                        pygame.draw.line(self.screen,(r-a,g,b),
                                     mouse.tail[a-1],
                                     mouse.tail[a],10-a*10//10)
            
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    Viewer(1430,800).run() # try Viewer(800,600).run()

