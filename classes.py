import json
import pygame
from pygame.locals import *
from types import SimpleNamespace

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
        self.moving = DirectionManager()

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:    # move left
                self.moving.left = True
            if event.key == K_d:    # move right
                self.moving.right = True
            if event.key == K_w:    # move up
                self.moving.up = True
            if event.key == K_s:    # move down
                self.moving.down = True

        if event.type == KEYUP:
            if event.key == K_a:    # move left
                self.moving.left = False
            if event.key == K_d:    # move right
                self.moving.right = False
            if event.key == K_w:    # move up
                self.moving.up = False
            if event.key == K_s:    # move down
                self.moving.down = False

    def update(self):

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
            self.pos.y -= 1
        if self.moving.down:
            self.pos.y += 1
        if self.moving.right:
            self.pos.x += 1
        if self.moving.left:
            self.pos.x -= 1

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.image.get_rect(center=self.pos))
