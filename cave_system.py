"""
author: Paul Polaschek
email: paul.plaschek@gmail.com
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/PaulPolaschek/Cave_system
"""


import pygame
import random
import os
#import time
import math

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
        if "msg" not in kwargs:
            self.msg = ""

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
        self._layer = 7
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
        # if bossnumber of cannon == 0: 
        #    cannon is from player and aims at mouse
        # else:
        #    cannon aims at player (number==0)
        mousevector = pygame.math.Vector2(0,0)
        if self.bossnumber ==  0:
             # it's the cannon of player1
             mousevector = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                       -pygame.mouse.get_pos()[1])
             
        elif 0 in VectorSprite.numbers:
             mousevector = VectorSprite.numbers[0].pos
             # its an enemy cannon and should aim at player
        diffvector = mousevector - self.pos
        angle = rightvector.angle_to(diffvector)
        self.set_angle(angle)
        
        if self.bossnumber != 0:
            # shoot !!!! at player !!!
            if not Game.peace and random.random() < 0.1:
                m = pygame.math.Vector2(50,0)
                m.rotate_ip(self.angle)
                # rocket should start at the tip of cannon barrel, not at cannon center
                p = pygame.math.Vector2(25,0)
                p.rotate_ip(self.angle)
                EnemyRocket(pos=self.pos+p, angle = self.angle, move=m)
        
class Turret(VectorSprite):
    
    def create_image(self):
        self.image = pygame.Surface((20,20))
        pygame.draw.circle(self.image, (250,0,0), (10,10), 10)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        
    def kill(self):
        VectorSprite.kill(self)
        Explosion(pos = self.pos, red = 200, dred = 50, minsparks = 50, maxsparks = 100, max_age = 1)

class NumberSprite(VectorSprite):
    
    def _overwrite_parameters(self):
        self.old = 0
        self.sign = 1
        self.size = 60
        self.shrinkspeed = 5
        self.shrinkduration = 5
   
    def create_image(self):
        ##make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
        
        d = ((int(self.age * self.shrinkspeed )) % self.shrinkduration)    # factor behind self.age = speed. number behind % = duration
        if d < self.old:
            # huch.... schrumpfung
            self.sign *= -1
        self.old = d
        self.size += d * self.sign
        #print("Size is :", self.size)
        self.image = make_text(msg = self.msg, fontsize = self.size, fontcolor=(random.randint(80,150),0,random.randint(180,250))) 
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        oldcenter = self.rect.center
        self.create_image()
        self.rect.center = oldcenter
   
    
    
 
class Guardian(VectorSprite):
    
    def _overwrite_parameters(self):
        self.speed = random.randint(5,15)
        v = pygame.math.Vector2(self.speed)
        v.rotate_ip(random.randint(0,360))
        self.move = v
        self.anchor = pygame.math.Vector2(self.pos.x, self.pos.y)
        self.max_dist = 100
    
    def create_image(self):
        self.image = pygame.Surface((30,30))
        pygame.draw.circle(self.image, (255,0,255), (15,15), 15)
        pygame.draw.circle(self.image, (0,0,255), (15,15), 5)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        # ----
        #if random.random() < 0.05:
        #    self.move.rotate_ip(random.randint(0,360))
        # ----
        dist = self.anchor - self.pos
        if dist.length() > self.max_dist:
            self.move = pygame.math.Vector2(dist.x,dist.y)
            self.move.normalize_ip()
            self.move *= self.speed
            
        

class Player(VectorSprite):
    
    def _overwrite_parameters(self):
        self.rotdelta = 1
        self.rot = 255
        self.mass = 400
        self.radius = 25
        self._layer = 8
        self.hitpoints = Game.playerhitpoints
        self.gravity = pygame.math.Vector2(0, -0.1)
        self.oldpos = pygame.math.Vector2(self.pos.x,self.pos.y)
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
                Viewer.sounds["playershooting"].play()
                Rocket(pos=p+t, move = v, angle = b, max_distance = Game.rocket_range,  bossnumber=0)
       
    def move_forward(self):
        v = pygame.math.Vector2(Game.playerspeed,0)
        v.rotate_ip(self.angle)
        self.move += v
        Flame(bossnumber=self.number, pos = self.pos)
        #if random.random() < 0.2:
            #Smoke(pos = self.pos, gravity = None, max_age=3.0)
            
        
    
    def create_image(self):
        self.image = pygame.Surface((Game.tilesize,Game.tilesize))
        pygame.draw.polygon(self.image, (255, 255, 0), ((0,0),(Game.tilesize,Game.tilesize//2),(0,Game.tilesize),(Game.tilesize//2,Game.tilesize//2)))
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
       
    def kill(self):
        Game.peace = True
        VectorSprite.kill(self)
        Explosion(pos = self.pos, red = 255, green = 255, minsparks = 400, maxsparks = 500, max_age = 3)
    
    def update(self, seconds):
        self.oldpos = pygame.math.Vector2(self.pos.x, self.pos.y)
        VectorSprite.update(self, seconds)
        oldcenter = self.rect.center
        self.create_image() 
        self.rect.center = oldcenter
        self.set_angle(self.angle)
        # gravity:
        self.move += self.gravity
        if self.hitpoints > Game.playerhitpoints:
            self.hitpoints = Game.playerhitpoints

        
class Tile(VectorSprite):
    
    def _overwrite_parameters(self):
        #self.tile_status = 0
        self._layer = 1 # so that player will be over Tile, not below it
        if self.tile_status == 0:
            self.hitpoints, self.hitpoints_old = 200, 200
        elif self.tile_status == 1:
        #if random.random() < 0.1:
            self.hitpoints, self.hitpoints_old = 800, 800
        #    self.tile_status = 1
        elif self.tile_status == 2:
            self.hitpoints, self.hitpoints_old = 100, 100
        #    self.tile_status = 2
        
        self.static = True
    
    def update(self, seconds):
        VectorSprite.update(self, seconds)    
        if self.hitpoints < self.hitpoints_old:
            oldcenter = self.rect.center
            self.create_image()
            self.rect.center = oldcenter
            self.hiptoins_old = self.hitpoints_old
    
    def create_image(self):
        self.image = pygame.Surface((Game.tilesize,Game.tilesize))
        if self.tile_status == 1:
            color = (255,165,0)
        elif self.tile_status == 2:
            color = (0,255,0)
            hppercent = self.hitpoints / 100
            g = max(0, 255 * hppercent)
            r = 255 - g
            color = (r,g,0)
        else:
            c = max(0, 255-self.hitpoints)
            c = min(255, 255-self.hitpoints) 
            #print("c=",c)
            color = (100,100,100)
        self.image.fill(color)
        pygame.draw.rect(self.image, (255,255,255), (0,0,Game.tilesize,Game.tilesize), 1)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
        

       
class Flame(VectorSprite):
    """ engine flame for spaceship"""    
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
        try:
            self.set_angle(VectorSprite.numbers[self.bossnumber].angle-180)
        except:
            print("problem with bossnumber", self.bossnumber)

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
        self.damage = 500
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
        

class EnemyRocket(Rocket):
    
    def create_image(self):
        self.image = pygame.Surface((10,5))
        pygame.draw.polygon(self.image, (255, 0, 128),
            [(0,0),(7,0),(10,2),(10,3),(7,4),(0,4)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
    
class Game():
    
    menu = []
    playermenu = ["back","hitpoints","speed","rockets","rocketspeed","increase shootingangle","decrease shootingangle"]
    mainmenu = ["play", "player1 settings", "level settings", "video settings", "exit game"]
    levelmenu = ["back", "tile size", "rooms", "holes", "circles", "rects"]
    videomenu = ["back", "640x400", "800x600", "1024x800", "1280x1024"]
    tilesizemenu = ["back to level menu", "5", "10", "15", "20", "25", "30"]
    manymenu = ["back to level menu", "none", "few", "many", "lots"]
    
    rockets = 1
    playerhitpoints = 1000
    playerspeed = 1
    rocketspeed = 1
    shooting_angle = 20
    gold = 0
    price = 10
    tilesize = 20
    rocket_range = 200
    rooms = "many"
    holes = "many"
    circles = "none"
    rects = "none"
    peace = False

class Viewer():
    width = 0
    height = 0
    sounds =   {}
    

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.mixer.pre_init(44100, -16, 2, 2048)
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
        # ------- background music -----
        self.songs = []
        self.song_index = -1
        try:
            for root, dirs, files in os.walk("data"):
                for file in files:
                    if file[-4:] == ".ogg":
                        self.songs.append(file)
            random.shuffle(self.songs) # remix sort order
        except:
            print("no folder 'data' or no ogg files in it")
        
        
        
        
        #Viewer.bombchance = 0.015
        #Viewer.rocketchance = 0.001
        Viewer.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.levels = {}
        #self.active_level = 0
        for i in range(3):
            self.active_level = i
            self.generate_level()
            self.levels[i] = self.lines
        self.active_level = 0
            
        self.prepare_sprites()
        self.lines = self.levels[0]
        self.paint_level() # painted current self.lines 
        self.prepare_sounds()
        self.loadbackground()
        Game.menu = Game.mainmenu[:]

    def next_song(self):
        self.song_index += 1
        if self.song_index >= len(self.songs):
            self.song_index = 0
        pygame.mixer.music.load(os.path.join("data", self.songs[self.song_index]))
        pygame.mixer.music.play()
        Flytext(x = 700, y = 100, text = "now playing: {}".format(self.songs[self.song_index]),  color = (255,0,0), fontsize = 100)
        

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
        
            
    def generate_level(self):
        """legend:
          0.... grey tile
          1.... golden tile
          2.... green tile
          @.... player start
          !.... turret
          +.... guardian
          A.... teleport source
          a.... teleport destination
          Bb, Cc etc ... teleports
          """
        xtiles = (Viewer.width-10) // Game.tilesize
        ytiles = (Viewer.height-30) // Game.tilesize
        self.lines = []
        for y in range(ytiles):
            line = []
            for x in range(xtiles):
                what = random.choice((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,2))
                line.append(str(what))
            self.lines.append(line)
        #print(self.lines) # level is in self.lines
        howmuch = {"none": 0,
                   "few" : 5,
                   "many": 10,
                   "lots": 15 }
        
        #------ kill all enemies -----
        #for e in self.enemygroup:
        #     e.kill()
            
                
        # ---- create rectangular room ----
        for _ in range(howmuch[Game.rooms]):
            x = random.randint(0, len(line))
            y = random.randint(0, len(self.lines))
            w = random.randint(5,10)
            h = random.randint(5,10)
            self.rectangle_hole(x, y, w, h )
            #if random.random() < 1:
            #    Turret(pos=pygame.math.Vector2((x)*Game.tilesize, -(y)*Game.tilesize))
            #if random.random() < 1:
            #    xg = (x - w // 2 ) * Game.tilesize #+10
            #    yg = (y - h // 2 ) * Game.tilesize #-30
            #    Guardian(pos = pygame.math.Vector2(xg,-yg))
        # ---- create round room (hole) -------
        for _ in range(howmuch[Game.holes]):
            self.round_hole(random.randint(5, len(line)-5), random.randint(5, len(self.lines)-5), random.randint(2,5))
        #round hole for player
        self.round_hole(len(line)//2, len(self.lines)//2, 4)
        #self.round_hole(40,9, 8)
        # circles
        
        # rects 
        
        #----- teleports
        if self.active_level == 0:
            #self.lines[random.randint(0,ytiles)][random.randint(0,xtiles)] = "A"
            x=random.randint(0, xtiles)
            y=random.randint(0, ytiles)
            char = self.lines[y][x]
            #if char in ".0":
            self.lines[y][x] = "A"
        elif self.active_level == 1:
            x=random.randint(0, xtiles)
            y=random.randint(0, ytiles)
            char = self.lines[y][x]
            #if char in ".0":
            
            for dy in range(-2,3):
                for dx in range(-2,3):
                    try:
                        self.lines[y+dy][x+dx] = "."
                    except:
                        pass
            self.lines[y][x] = "a"
            
            
            
            x=random.randint(0, xtiles)
            y=random.randint(0, ytiles)
            char = self.lines[y][x]
            
            #if char in ".0":
            self.lines[y][x] = "B"
        elif self.active_level == 2:
            x=random.randint(0, xtiles)
            y=random.randint(0, ytiles)
            print(x, y)
            char = self.lines[y][x]
            #if char in ".0":
            for dy in range(-2,3):
                for dx in range(-2,3):
                    try:
                        self.lines[y+dy][x+dx] = "."
                    except:
                        pass
            
            self.lines[y][x] = "b"
        
            
        
        # ---- cannon for each enemy1
        #for e in self.enemygroup:
        #    Cannon(bossnumber = e.number) 
        #print("das ist self.lines")
        #print(self.lines)
        #self.levels.append(self.lines)        
        #self.paint_level()
                
        
    def paint_level(self):
         # kill old tiles 
         for t in self.tilegroup:
             t.kill()
         # generate new tiles
         for y, line in enumerate(self.lines):
              for x, char in enumerate(line):
                  p = pygame.math.Vector2(x*Game.tilesize + 10, -y*Game.tilesize - 30)
                  if char == "0" or char=="1" or char =="2":
                      Tile(pos=p, tile_status=int(char))
                  elif char in "abcABC":
                      NumberSprite(pos=p, msg=char)
                      
          #for x in range(10, Viewer.width, 20):
          #  for y in range(30, Viewer.height, 20):
          #      Tile(pos=pygame.math.Vector2(x, -y), color=(16,16,16))
   
    def change_level(self, level_nr):
        """changes into level # level_nr"""
        self.lines = self.levels[level_nr]
        for n in self.numbergroup:
            n.kill()
        self.paint_level() # painted current self.lines 
                    
    def go_to_teleport(self, teleport):
        """moves player to teleport with letter in teleport"""
        for n in self.numbergroup:
                                if n.msg == teleport:
                                    self.player1.pos = pygame.math.Vector2(n.pos.x, n.pos.y)
    
    def prepare_sounds(self):
        
        Viewer.sounds["hitground"] = pygame.mixer.Sound(os.path.join("data", "player_hits_ground.wav"))
        Viewer.sounds["playershooting"] = pygame.mixer.Sound(os.path.join("data", "player_shooting.wav"))
        Viewer.sounds["playerdamage"] = pygame.mixer.Sound(os.path.join("data", "player_takes_damage.wav"))
        Viewer.sounds["playerhealing"] = pygame.mixer.Sound(os.path.join("data", "player_healing.wav"))
        Viewer.sounds["enemydamage"] = pygame.mixer.Sound(os.path.join("data", "enemy_takes_damage.wav"))
        
    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.mousegroup = pygame.sprite.Group()
        #self.monstergroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        #self.lasergroup = pygame.sprite.Group()
        self.flytextgroup = pygame.sprite.Group()
        self.tilegroup = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.guardiangroup = pygame.sprite.Group()
        self.numbergroup = pygame.sprite.Group()
        
        Mouse.groups = self.allgroup, self.mousegroup
        #EvilMonster.groups = self.allgroup, self.monstergroup
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        Player.groups = self.allgroup, self.playergroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Spark.groups = self.allgroup
        #Smoke.groups = self.allgroup
        Flame.groups = self.allgroup
        #EvilLaser.groups = self.allgroup, self.lasergroup
        Tile.groups = self.allgroup, self.tilegroup
        Turret.groups = self.allgroup, self.enemygroup
        Guardian.groups = self.allgroup, self.guardiangroup
        NumberSprite.groups = self.allgroup, self.numbergroup

   
        # ------ player1,2,3: mouse, keyboard, joystick ---
        self.player1 =  Player(bounce_on_edge = True, pos=pygame.math.Vector2(Viewer.width/2,-Viewer.height/2))
        self.cannon1 = Cannon(bossnumber=self.player1.number)
        print("cannon1 has number", self.cannon1.number)
        self.mouse1 = Mouse(control="mouse", color=(255,0,0))
        #self.mouse2 = Mouse(control='keyboard1', color=(255,255,0))
        #self.mouse3 = Mouse(control="keyboard2", color=(255,0,255))
        #self.mouse4 = Mouse(control="joystick1", color=(255,128,255))
        #self.mouse5 = Mouse(control="joystick2", color=(255,255,255))

        #xtiles = (Viewer.width-10) // 20
        #ytiles = (Viewer.height-30) // 20
        #self.generate_level(xtiles, ytiles)
        #self.paint_level()
        self.generate_level()
        
        #for x in range(20):
        #    EvilMonster(bounce_on_edge=True)
      
    def draw_spaceship(self):
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
            
    
    def calculate_price(self, cursor):
        text = Game.menu[cursor]
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
   
    def menurun(self):
        running = True
        cursor = 0
        lastmenu = None
        while running:
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000# - self.menudeltatime
            
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
                        cursor = min(len(Game.menu)-1, cursor)
                        self.calculate_price(cursor)
                    if event.key == pygame.K_UP:
                        cursor -= 1
                        cursor = max(0, cursor)
                        self.calculate_price(cursor) 
                        #running = False
                    if event.key == pygame.K_RETURN:
                        #Flytext(500, 500, text=Game.menupoints[cursor])
                        text = Game.menu[cursor]
                        if text == "play":
                            return
                        elif text == "exit game":
                            running = False
                        elif text == "player1 settings":
                            Game.menu = Game.playermenu[:]
                            cursor = 0
                        elif text == "back":
                            Game.menu = Game.mainmenu[:]
                            cursor = 0
                        elif text == "video settings":
                            Game.menu = Game.videomenu[:]
                            cursor = 0
                        elif text == "level settings":
                            Game.menu = Game.levelmenu[:]
                            cursor = 0
                        elif text == "tile size":
                            lastmenu = "tile size"
                            Game.menu = Game.tilesizemenu[:]
                            cursor = 0
                        elif text == "rooms":
                            Game.menu = Game.manymenu[:]
                            cursor = 0
                            lastmenu = "rooms"
                        elif text == "holes":
                            Game.menu = Game.manymenu[:]
                            cursor = 0
                            lastmenu = "holes"
                        elif text == "circles":
                            Game.menu = Game.manymenu[:]
                            cursor = 0
                            lastmenu = "circles"
                        elif text == "rects":
                            Game.menu = Game.manymenu[:]
                            cursor = 0
                            lastmenu = "rects"
                        elif text == "back to level menu":
                            Game.menu = Game.levelmenu[:]
                            cursor = 0
                        elif text == "none":
                            if lastmenu == "rects":
                                Game.rects = "none"
                            elif lastmenu == "circles":
                                Game.circles = "none"
                            elif lastmenu == "rooms":
                                Game.rooms = "none"
                            elif lastmenu == "holes":
                                Game.holes = "none"
                            self.generate_level()
                        elif text == "few":
                            if lastmenu == "rects":
                                Game.rects = "few"
                            elif lastmenu == "circles":
                                Game.circles = "few"
                            elif lastmenu == "rooms":
                                Game.rooms = "few"
                            elif lastmenu == "holes":
                                Game.holes = "few"
                            self.generate_level()
                        elif text == "many":
                            if lastmenu == "rects":
                                Game.rects = "many"
                            elif lastmenu == "circles":
                                Game.circles = "many"
                            elif lastmenu == "rooms":
                                Game.rooms = "many"
                            elif lastmenu == "holes":
                                Game.holes = "many"
                            self.generate_level()
                        elif text == "lots":
                            if lastmenu == "rects":
                                Game.rects = "lots"
                            elif lastmenu == "circles":
                                Game.circles = "lots"
                            elif lastmenu == "rooms":
                                Game.rooms = "lots"
                            elif lastmenu == "holes":
                                Game.holes = "lots"
                            self.generate_level()
                        
                        elif text in ["5", "10", "15", "20", "25", "30"]:
                            if lastmenu == "tile size":
                                Game.tilesize = int(text)
                                Flytext(500,400,"Tilesize is now : {}".format(text), fontsize=40, color=(128,0,128))
                                self.generate_level()
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
            Game.gold, Game.price, Game.rockets, Game.shooting_angle, Game.playerspeed, self.clock.get_fps() ), x=10, y=10, color = (255,255,255))
            
            #---- draw shootingangle
            if Game.menu == Game.playermenu:
                self.draw_spaceship()
            
            # ---------------- 
            self.flytextgroup.update(seconds)
            

            # draw menu
            for a, line in enumerate(Game.menu):
                write(self.screen, line, x=200, y= 100+a*25, color = (255,255,255))
            c = random.randint(200, 255)   #, random.randint(0,255), random.randint(0,255))
            write(self.screen, "--->", x = 120, y = 100+cursor * 25, color = (c,c,c))
            pygame.display.flip()
        # --- menu fertig -----
        # exit pygame
        #pygame.mouse.set_visible(True)    
        #pygame.quit()
        return -1
   
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
        self.next_song() # play next song
        NumberSprite(pos = pygame.math.Vector2(100,-100))
        
        #self.menutime = False
        #self.menudeltatime = 0
        while running:
            milliseconds = self.clock.tick(self.fps) #
            #if self.menutime:
            #    self.menudeltatime += milliseconds / 1000
            #    self.menutime = False
            seconds = milliseconds / 1000 #- self.menudeltatime
            #self.menudeltatime = 0
            #else:
            #    seconds = milliseconds / 1000
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
                    if event.key == pygame.K_1:
                        self.change_level(0)
                        #self.lines = self.levels[0]
                        #self.paint_level() # painted current self.lines 
                    if event.key == pygame.K_2:
                        self.change_level(1)
                        #self.lines = self.levels[1]
                        #self.paint_level() # painted current self.lines 
                    if event.key == pygame.K_3:
                        self.change_level(2)
                        #self.lines = self.levels[2]
                        #self.paint_level() # painted current self.lines 
                    if event.key == pygame.K_p:
                        if not Game.peace:
                            Game.peace = True
                        else:
                            Game.peace = False
                    if event.key == pygame.K_i:
                        self.next_song()
                    if event.key == pygame.K_o:
                        Viewer.sounds["hitground"].play()
                    if event.key == pygame.K_n:
                        self.generate_level()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_TAB:
                        self.player1.fire(self.cannon1.angle)
                    if event.key == pygame.K_m:
                        #self.menutime = True
                        result = self.menurun()
                        if result == -1:
                            running = False
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
            
            if right:
                self.player1.move_forward()
            
            oldleft, oldmiddle, oldright = left, middle, right

          
            
            self.allgroup.update(seconds)


            
            # ======== collision detections ============
            if 0 in VectorSprite.numbers:
                #----- between Tile and player ------
                for p in self.playergroup:
                    crashgroup = pygame.sprite.spritecollide(p, self.tilegroup,
                                 False, pygame.sprite.collide_rect)
                    for t in crashgroup:
                         # elastic_collision(p, m)
                         t.hitpoints -= 1
                         if t.tile_status == 2:
                             #healing tile
                            p.hitpoints += 1
                            Viewer.sounds["playerhealing"].play()
                         else:
                             p.hitpoints -= 1
                             Viewer.sounds["hitground"].play()
                             Explosion(t.pos, red=200, dred=50, minsparks=1, maxsparks=2)
                         #elastic_collision(t,p)                    
                         #v = p.move * -1
                         #ok = True
                         #try: 
                         #   v.normalize_ip()
                         #except:
                         #    ok = False
                         #if ok:
                         #   v *= 4 # distance to wall
                         #   p.pos += v
                         #   #p.pos += (p.move * -1)
                         p.pos = pygame.math.Vector2(p.oldpos.x, p.oldpos.y)
                         p.move = pygame.math.Vector2(0,0)
                         p.rect.center = ( round(p.pos.x, 0), -round(p.pos.y, 0) )
                         self.cannon1.update(0)
                         #self.cannon1.pos = pygame.math.Vector2(p.pos.x, p.pos.y)
                         #self.cannon1.center = p.rect.center
                        
                
                #------ between Tile and rocket ------
                for r in self.rocketgroup:
                    crashgroup = pygame.sprite.spritecollide(r, self.tilegroup,
                                False, pygame.sprite.collide_rect)
                    for t in crashgroup:
                        print("r.bossnr, t.tilest", r.bossnumber, t.tile_status)
                        if r.bossnumber == 0:
                            if t.tile_status == 0:
                                print("hitting normal tile")
                                # normal
                                b1 = r.angle -45 + 180
                                b2 = r.angle + 45 + 180
                                Viewer.sounds["hitground"].play()
                                Explosion(r.pos, a1=b1, a2=b2, max_age=0.3, red=128, green=128, blue=128, dred=15, dgreen = 15, dblue = 15, minsparks=1, maxsparks=2)
                                t.hitpoints -= r.damage
                            elif t.tile_status == 1:
                                # golden
                                b1 = r.angle -45 + 180
                                b2 = r.angle + 45 + 180
                                Viewer.sounds["hitground"].play()
                                Explosion(r.pos, a1=b1, a2=b2, max_age=0.3, red=255, green=165, blue=0, dred=15, dgreen = 15, dblue = 15, minsparks=1, maxsparks=2)
                                t.hitpoints -= r.damage
                            else:
                                # healing
                                Viewer.sounds["playerhealing"].play()
                                VectorSprite.numbers[r.bossnumber].hitpoints += r.damage    
                                b1 = r.angle -45 + 180
                                b2 = r.angle + 45 + 180
                                Explosion(r.pos, a1=b1, a2=b2, max_age=0.3, red=0, green=255, blue=0, dred=15, dgreen = 15, dblue = 15, minsparks=1, maxsparks=2)
                                t.hitpoints -= r.damage
                        r.kill()
                
                #------ between player and rocket ------
                for p in self.playergroup:
                    crashgroup = pygame.sprite.spritecollide(p, self.rocketgroup,
                                 False, pygame.sprite.collide_rect)
                    for r in crashgroup:
                        if r.bossnumber != 0:
                            p.hitpoints -= r.damage
                            b1 = r.angle -45 + 180
                            b2 = r.angle + 45 + 180
                            Viewer.sounds["playerdamage"].play()
                            Explosion(r.pos, a1=b1, a2=b2, max_age=0.3, red=200, dred=50, minsparks=1, maxsparks=2)
                        r.kill()
                
                #------ between player and NumberSprite ------
                for p in self.playergroup:
                    crashgroup = pygame.sprite.spritecollide(p,self.numbergroup,
                                 False, pygame.sprite.collide_rect)
                    for n in crashgroup:
                        
                        if n.msg == "A":
                            # teleport to level 1
                            self.change_level(level_nr = 1)
                            self.go_to_teleport(teleport = "a")
                        elif n.msg == "B":
                            # teleport to level 2
                            self.change_level(level_nr = 2)
                            self.go_to_teleport(teleport = "b")
                        
                    

                #------ between rocket and enemy ------
                for e in self.enemygroup:
                    crashgroup = pygame.sprite.spritecollide(e, self.rocketgroup,
                                 False, pygame.sprite.collide_rect)
                    for r in crashgroup:
                        if r.bossnumber == 0:
                            e.hitpoints -= r.damage
                            b1 = r.angle -45 + 180
                            b2 = r.angle + 45 + 180
                            Viewer.sounds["enemydamage"].play()
                            Explosion(r.pos, a1=b1, a2=b2, max_age=0.3, red=200, dred=50, minsparks=1, maxsparks=2)
                        r.kill()
                
                #------ between guardian and tile ----
                #for g in self.guardiangroup:
                #    crashgroup = pygame.sprite.spritecollide(g, self.tilegroup,
                #                 False, pygame.sprite.collide_rect)
                #    for t in crashgroup:
                #        print("crashing", g, t)
                #        g.pos += -g.move
                #        g.rect.center = (g.pos.x, -g.pos.y)
                #        g.move *= -1
                
            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)
            
            hppercent = self.player1.hitpoints / Game.playerhitpoints
            g = max(0, 255 * hppercent)
            g = min(255 * hppercent, 255)
            r = max(0, 255 - g)
            r = min(255 - g, 255)
            #print("g={}".format(255 * hppercent))
            pygame.draw.rect(self.screen, (255,255,0), (0,2,self.player1.hitpoints+4,16))
            pygame.draw.rect(self.screen, (r,g,0), (2,4,self.player1.hitpoints,12))
            
            # write text over sprites
            write(self.screen, "hp: {}".format(self.player1.hitpoints), x=10, y=2, fontsize=14)
            write(self.screen, "FPS: {:8.3}  rockets: {} gold: {}".format(self.clock.get_fps(),
            Game.rockets, Game.gold), x=1150, y=0, fontsize = 14, color = (255,255,255))
            
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

