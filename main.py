from typing import overload
import pygame
from pygame.locals import *

class Game(object):

    WIDTH = 480
    HEIGHT = 480
    FPS = 30

    # Define Colors 
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self,gameStates = []) -> None:
        ## initialize pygame and create window
        pygame.init()
        pygame.mixer.init()  ## For sound
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bot Invasion")
        self.clock = pygame.time.Clock()     ## For syncing the FPS
        self.running = True
        self.font = pygame.font.Font("assets/pixel_reg.ttf",18)
        self.game_states = gameStates
        # print("Game Initialized")
        pass
    
    def handle_events(self):
            # print("i am game events >:)")
            for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
                ## listening for the the X button at the top
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    self.keys_pressed = pygame.mouse.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            # print("Game Events handled")
    
    def update(self):
        # print("Game Updated")
        pass

    def draw(self):
        self.screen.fill(self.BLACK)
        # print("Game Drawn")
    
    def run(self):
            # print("--------------------")
            self.clock.tick(self.FPS)
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()

class MainScreen(Game):

    def __init__(self):
        super().__init__()
        self.gotonext = False
        # print("MainScreen here!")
        pass

    
    def handle_events(self):
        for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
            ## listening for the the X button at the top
            if event.type == pygame.QUIT:
                    self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == K_RIGHT:
                    self.gotonext = True
            if event.type == MOUSEBUTTONDOWN:
                self.keys_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        # print("MainScreen Events handled")

    def update(self):
        self.title_text = self.font.render("Main Screen",False,self.WHITE)
    
    def draw(self):
        self.screen.fill((0,200,0))
        self.screen.blit(self.title_text,(2,2))
        # print("MainScreen Drawn")

class PlayScreen(Game):

    def __init__(self):
        super().__init__()
        self.gotonext = False
        # print("Playscreen here!")
        pass
    
    def handle_events(self):
        for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
            ## listening for the the X button at the top
            if event.type == pygame.QUIT:
                    self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == K_RIGHT:
                    self.gotonext = True
            if event.type == MOUSEBUTTONDOWN:
                self.keys_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        # print("MainScreen Events handled")

    def update(self):
        self.title_text = self.font.render("Play Screen",False,self.WHITE)

    def draw(self):
        self.screen.fill((0,0,200))
        self.screen.blit(self.title_text,(2,2))
        # print("MainScreen Drawn")

class EndScreen(Game):

    def __init__(self):
        super().__init__()
        # print("EndScreen here")
        self.gotonext = False
        pass
    
    def handle_events(self):
        for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
            ## listening for the the X button at the top
            if event.type == pygame.QUIT:
                    self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == K_RIGHT:
                    self.gotonext = True
            if event.type == MOUSEBUTTONDOWN:
                self.keys_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        # print("EndScreen Events handled")

    def update(self):
        self.title_text = self.font.render("End Screen",False,self.WHITE)

    def draw(self):
        self.screen.fill((200,0,0))
        self.screen.blit(self.title_text,(2,2))
        # print("EndScreen Drawn")

class GameState:
    def __init__(self,state:str,new:bool = True):
        self.state = state
        self.new = new
    def getState(self):
        if "main" in self.state:
            return MainScreen()
        elif "play" in self.state:
            return PlayScreen()
        elif "end" in self.state:
            return EndScreen()


gamestates = [GameState("mainscreen"),GameState("playscreen"),GameState("endscreen")]
state_id = 0
game = gamestates[state_id].getState()
while game.running:
    if game.gotonext:
        game.gotonext = False
        state_id += 1
        if state_id > (len(gamestates)-1):
            state_id = 0
        game = gamestates[state_id].getState()
    game.run()