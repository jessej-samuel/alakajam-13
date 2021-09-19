import pygame
from pygame.locals import *
from classes import *
import random


class Game(object):

    WIDTH = 480
    HEIGHT = 480
    FPS = 60

    # Define Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    VIOLET = (12,12,12)

    def __init__(self, gameStates=[]) -> None:
        # initialize pygame and create window
        pygame.init()
        pygame.mixer.init()  # For sound
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bot Invasion")
        self.clock = pygame.time.Clock()  # For syncing the FPS
        self.running = True
        self.font = pygame.font.Font("assets/pixel_reg.ttf", 32)
        self.game_states = gameStates

        # print("Game Initialized")
        pass

    def handle_events(self):
        # print("i am game events >:)")
        # gets all the events which have occured till now and keeps tab of them.
        for event in pygame.event.get():
            # listening for the the X button at the top
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

        # Rendering stuff
        self.title_text = self.font.render("Main Screen", False, self.WHITE)
        self.title_image = pygame.image.load("assets/TITLE.png").convert()
        self.title_image.set_colorkey((0, 0, 0))
        self.yoff = 0
        self.change = 0.5
        self.start_prompt = self.font.render(
            "Press any key to start...", False, self.WHITE)
        self.start_prompt_rect = self.start_prompt.get_rect(
            center=(int(self.WIDTH/2), int(self.HEIGHT/2)))

        # Music
        pygame.mixer.music.load("assets/tb303_01.ogg")
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)
        # print("MainScreen here!")
        pass

    def handle_events(self):
        # gets all the events which have occured till now and keeps tab of them.
        for event in pygame.event.get():
            # listening for the the X button at the top
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                else:
                    self.gotonext = True
            if event.type == MOUSEBUTTONDOWN:
                self.keys_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        # print("MainScreen Events handled")

    def update(self):
        # self.yoff += self.change
        pass

    def draw(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.title_text, (2, 2))
        self.screen.blit(self.title_image, (50, 50))
        self.screen.blit(self.start_prompt, self.start_prompt_rect)
        # print("MainScreen Drawn")


class PlayScreen(Game):

    def __init__(self):
        super().__init__()
        # self.frames = 0
        self.gotonext = False
        # Music
        pygame.mixer.music.load("assets/techno_bass02.ogg")
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)

        # Botty stuff
        self.botty = Botty("assets/botty")

        # print("Playscreen here!")

    def handle_events(self):
        # gets all the events which have occured till now and keeps tab of them.
        for event in pygame.event.get():
            # listening for the the X button at the top
            if event.type == pygame.QUIT:
                self.running = False

            # Botty events
            self.botty.handle_events(event)

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
        self.botty.update()
        self.title_text = self.font.render("Moving" if self.botty.moving.is_moving else "", False, self.WHITE)
        self.botty.moving.update()
        

    def draw(self):
        self.screen.fill(self.VIOLET)
        self.screen.blit(self.title_text, (2, 2))
        self.botty.draw(self.screen)
        # print("MainScreen Drawn")


class EndScreen(Game):

    def __init__(self):
        super().__init__()
        # print("EndScreen here")
        self.gotonext = False
        # Music
        pygame.mixer.music.load("assets/break03.ogg")
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)
        pass

    def handle_events(self):
        # gets all the events which have occured till now and keeps tab of them.
        for event in pygame.event.get():
            # listening for the the X button at the top
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
        self.title_text = self.font.render("End Screen", False, self.WHITE)

    def draw(self):
        self.screen.fill((200, 0, 0))
        self.screen.blit(self.title_text, (2, 2))
        # print("EndScreen Drawn")


class GameState:
    def __init__(self, state: str, new: bool = True):
        self.state = state
        self.new = new

    def getState(self):
        if "main" in self.state:
            return MainScreen()
        if "play" in self.state:
            return PlayScreen()
        if "end" in self.state:
            return EndScreen()

if __name__ == '__main__':
    gamestates = [GameState("mainscreen"), GameState(
        "playscreen"), GameState("endscreen")]
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
