import json
import pygame
from pygame.locals import *
from types import SimpleNamespace

# Parse JSON into an object with attributes corresponding to dict keys.
# x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
# print(x.name, x.hometown.name, x.hometown.id)

class Spritesheet:

    def __init__(self,filename:str):
        self.sheet = pygame.image.load(filename+".png").convert()
        self.sheet.set_colorkey((0,0,0))
        self.sprites = []
        self.json_data = open(filename+".json").read()
        self.data = json.loads(self.json_data, object_hook=lambda d: SimpleNamespace(**d))
        # print(self.data.frames[0].frame)
        for frame in self.data.frames:
            self.sprites.append(self.sheet.subsurface(Rect(frame.frame.x,frame.frame.y,frame.frame.w,frame.frame.h)))
        self.duration = self.data.frames[0].duration

class Botty:
    def __init__(self,filename):
        self.ss = Spritesheet(filename)
        self.index = 0
        self.image = self.ss.sprites[self.index]
        self.time = 0
        self.duration = 60
    
    def update(self):
        self.time += 1
        if self.time >= self.duration:
            self.time = 0
            self.index += 1
            if self.index > len(self.ss.sprites)-1:
                self.index = 0
        self.image = self.ss.sprites[self.index]