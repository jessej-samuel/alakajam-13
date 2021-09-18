import pygame
from pygame.locals import *

class Spritesheet:

    def __init__(self,sheet_path:str):
        self.sheet = pygame.image.load(sheet_path).convert()