import json
import pygame
from pygame.locals import *
from types import SimpleNamespace
import random

# Parse JSON into an object with attributes corresponding to dict keys.
# x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
# print(x.name, x.hometown.name, x.hometown.id)


class DirectionManager(object):

    def __init__(self):
        self.up = self.down = self.left = self.right = self.is_moving = False

    def update(self):
        if self.up or self.down or self.right or self.left:
            self.is_moving = True
        else:
            self.is_moving = False


class Spritesheet:

    def __init__(self, filename: str):
        self.sheet = pygame.image.load(filename+".png").convert()
        self.sheet.set_colorkey((0, 0, 0))
        self.sprites = []
        self.json_data = open(filename+".json").read()
        self.data = json.loads(
            self.json_data, object_hook=lambda d: SimpleNamespace(**d))
        for frame in self.data.frames:
            self.sprites.append(self.sheet.subsurface(
                Rect(frame.frame.x, frame.frame.y, frame.frame.w, frame.frame.h)))
        self.duration = self.data.frames[0].duration


class Botty:

    def __init__(self, filename):
        WIDTH = HEIGHT = 480
        self.ss = Spritesheet(filename)
        self.index = 0
        self.image = self.ss.sprites[self.index]
        self.time = 0
        self.duration = 60
        self.size = (
            self.ss.data.frames[self.index].sourceSize.w,
            self.ss.data.frames[self.index].sourceSize.h
        )
        self.pos = pygame.Vector2(WIDTH/2, HEIGHT/2)
        self.vel = pygame.Vector2(0,0)
        self.max_vel = 5
        self.acc = pygame.Vector2(0.0,0.0)
        self.moving = DirectionManager()
        self.rect = self.image.get_rect(center=self.pos)

        # Shooting stuff
        self.shooting = False
        self.bullets = []
        self.firing_timer = 0
        self.firing_rate = 10
        self.bots_killed = 0
        self.hp = 100
        self.hp_cooldown = 0
        self.is_hit = False

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:    # move left
                self.moving.left = True
                self.vel.x = -2
            if event.key == K_d:    # move right
                self.moving.right = True
                self.vel.x = 2
            if event.key == K_w:    # move up
                self.moving.up = True
                self.vel.y = -2
            if event.key == K_s:    # move down
                self.moving.down = True
                self.vel.y = 2

        if event.type == KEYUP:
            if event.key == K_a:    # move left
                self.moving.left = False
                if self.acc.x < 0:
                    self.acc.x = 0
                    self.vel.x = 0
            if event.key == K_d:    # move right
                self.moving.right = False
                if self.acc.x > 0:
                    self.acc.x = 0
                    self.vel.x = 0
            if event.key == K_w:    # move up
                self.moving.up = False
                if self.acc.y < 0:
                    self.acc.y = 0
                    self.vel.y = 0
            if event.key == K_s:    # move down
                self.moving.down = False
                if self.acc.y > 0:
                    self.acc.y = 0
                    self.vel.y = 0
        
        if event.type == MOUSEBUTTONDOWN:
            self.shooting = True

        if event.type == MOUSEBUTTONUP:
            self.shooting = False

    def update(self):
        self.moving.update()

        # Animation
        self.time += 1
        if self.time >= self.duration:
            self.time = 0
            self.index += 1
            if self.index > len(self.ss.sprites)-1:
                self.index = 0
        self.image: pygame.Surface = self.ss.sprites[self.index]

        # Movement
        if self.moving.up:
            self.acc.y = -0.02
        if self.moving.down:
            self.acc.y = 0.02
        if self.moving.right:
            self.acc.x = 0.02
        if self.moving.left:
            self.acc.x = -0.02
        
        self.vel += self.acc
        self.pos += self.vel
        if self.vel.x > self.max_vel:
            self.vel.x = self.max_vel
        if self.vel.y > self.max_vel:
            self.vel.y = self.max_vel
        
        if self.shooting:
            self.firing_timer += 1
            if self.firing_timer == self.firing_rate:
                self.firing_timer = 0
                self.shoot(pygame.mouse.get_pos())
        
        for bullet in self.bullets:
            if bullet.pos.x > 480 or bullet.pos.x < 0 or bullet.pos.y > 480 or bullet.pos.y < 0:
                bullet.is_alive = False
            if bullet.is_alive:
                bullet.update()
            else:
                self.bullets.remove(bullet)
        
        self.rect = self.image.get_rect(center=self.pos)
        self.hp_cooldown += 1

    def draw(self, screen: pygame.Surface):
        for bullet in self.bullets:
            bullet.draw(screen)
        screen.blit(self.image, self.image.get_rect(center=self.pos))
    
    def shoot(self,mouse_pos:pygame.Vector2):
        self.bullets.append(Bullet(self.pos, mouse_pos))

class Bullet(object):

    def __init__(self,shooter_pos:pygame.Vector2,mouse_pos:pygame.Vector2):
        self.damage = 2
        self.vel = mouse_pos - shooter_pos
        self.vel.scale_to_length(3)
        self.pos = pygame.Vector2(shooter_pos.x,shooter_pos.y)
        self.size = 2
        self.is_alive = True
        self.rect = Rect(self.pos.x - self.size,self.pos.y - self.size,self.size*2,self.size*2)
    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
    
    def draw(self,screen):
        pygame.draw.circle(screen,(255,255,255),self.pos,self.size)

class BlueBot(Botty):

    def __init__(self,filename:str,player:Botty):
        super().__init__(filename)
        self.player = player
        self.pos = pygame.Vector2(random.random()*20,random.random()*480)
        self.vel = pygame.Vector2((random.random()+0.01)*2*random.choice([-1,1]),(random.random()+0.01)*2*random.choice([-1,1]))
        # self.vel = (player.pos - self.pos).scale_to_length(2)
        self.acc = pygame.Vector2(0.01,0.01)
        self.alive = True
        self.hp = 50
    
    def handle_events(self, event):
        event = event
        return 

    def update(self):
        # Animation
        self.time += 1
        if self.time >= self.duration:
            self.time = 0
            self.index += 1
            if self.index > len(self.ss.sprites)-1:
                self.index = 0
        self.image: pygame.Surface = self.ss.sprites[self.index]

        if self.pos.y < 0 or self.pos.y > 480 or self.pos.x < 0 or self.pos.x > 480:
            self.alive = False

        self.vel = (self.player.pos - self.pos)
        self.vel.scale_to_length(0.5)
        self.pos += self.vel

        self.rect.center = self.pos

    def draw(self,screen):
        screen.blit(self.image, self.image.get_rect(center=self.pos))
        if self.is_hit:
            pygame.draw.circle(screen,(250,250,250),self.pos,8)
            self.is_hit = False

