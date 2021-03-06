import pygame
from pygame.locals import *
from classes import *
import random
import time

bots_killed,time_survived = 0,0

class Game(object):

    WIDTH = 480
    HEIGHT = 480
    FPS = 120

    # Define Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    VIOLET = (12, 12, 12)

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

        self.bots_killed = 0
        self.time_survived = 0

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
        self.current_time = str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)
        self.title_text = self.font.render(self.current_time, False, self.WHITE)
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
        time_ = time.localtime()
        self.current_time = str(time_.tm_hour)+":"+str(time_.tm_min)+":"+str(time_.tm_sec)
        self.title_text = self.font.render(self.current_time, False, self.WHITE)
        # self.yoff += self.change

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

        # background
        self.bg = pygame.image.load("assets/tilemap.png").convert()
        self.bg.fill((100,100,100),special_flags=BLEND_RGB_SUB)

        # Music
        pygame.mixer.music.load("assets/techno_bass02.ogg")
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)

        # Botty stuff
        self.botty = Botty("assets/botty")

        # BlueBot stuff
        self.bluebots = [BlueBot("assets/blue_bot",self.botty)]

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
            if event.type == MOUSEBUTTONDOWN:
                self.keys_pressed = pygame.mouse.get_pressed()
        if len(self.bluebots) < 20:
            self.bluebots.append(BlueBot("assets/blue_bot",self.botty))
        self.mouse_pos = pygame.mouse.get_pos()
        # print("MainScreen Events handled")

    def update(self):
        self.botty.update()
        self.title_text = self.font.render(str("Bots Killed: "+str(self.botty.bots_killed)), False, self.WHITE)
        for bluebot in self.bluebots:
            if self.botty.rect.colliderect(bluebot.rect):
                self.botty.is_hit = True
                if self.botty.hp_cooldown > 20:
                    self.botty.hp_cooldown = 0
                    self.botty.hp -= random.randint(2,5)
            else:
                self.botty.is_hit = False
            for bullet in self.botty.bullets:
                if bluebot.rect.colliderect(bullet.rect):   # on getting hit
                    bluebot.hp -= bullet.damage
                    bluebot.is_hit = True
                    if bluebot.hp <= 0:
                        bluebot.alive = False
            if not bluebot.alive:
                self.botty.bots_killed += 1
                self.bluebots.remove(bluebot)
                pass
            bluebot.update()
        self.hp_bar = Rect(0,0,self.botty.hp*2,18)
        self.hp_bar.topright = (480,0)
        if self.botty.hp <= 0:
            global bots_killed,time_survived
            bots_killed = self.botty.bots_killed
            time_survived = self.botty.time_survived
            self.gotonext = True

    def draw(self):
        # self.screen.fill(self.VIOLET)
        self.screen.blit(self.bg,(0,0))
        for bluebot in self.bluebots:
            bluebot.draw(self.screen)
        self.botty.draw(self.screen)
        self.screen.blit(self.title_text, (2, 2))
        pygame.draw.rect(self.screen,(255,0,0),self.hp_bar)
        
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
        self.title_text = self.font.render("Game Over!", False, self.WHITE)
        self.kills_text = self.font.render("Bots Killed: "+str(bots_killed), False, self.WHITE)
        self.time_text = self.font.render("Time Survived: "+str(round(time_survived/self.FPS,2))+" bot seconds", False, self.WHITE)

    def draw(self):
        self.screen.fill((20, 20, 20))
        self.screen.blit(self.title_text, (2, 2))
        self.screen.blit(self.kills_text,self.kills_text.get_rect(center = (self.WIDTH/2,self.HEIGHT/2+16)))
        self.screen.blit(self.time_text,self.time_text.get_rect(center = (self.WIDTH/2,self.HEIGHT/2-16)))
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
