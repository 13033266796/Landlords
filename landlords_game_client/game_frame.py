import pygame
import sys
import time
import threading
from pygame.locals import *


class GameFrame:
    def __init__(self):
        self.screen = pygame.display.set_mode([1133, 754])
        self.back_ground = pygame.image.load(r".\\source\\background\\backGround_1.png")
        self.screen.blit(self.back_ground, (0, 0))
        pygame.display.set_caption("斗地主")
        self.ready_gamer_num = 0
        self.status = "wait"

    def main_paint_loop(self):
        while True:
            if self.status == "wait":
                self.wait()
            if self.status == "qdz":
                pass

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self.screen.blit(self.back_ground, (0, 0))
            if self.ready_gamer_num == 0:
                player_ready = pygame.image.load(r"source\ok.png")
                self.screen.blit(player_ready, (500, 600))
            if self.ready_gamer_num == 1:
                pre_player_ready = pygame.image.load(r"source\ok.png")
                player_ready = pygame.image.load(r"source\ok.png")
                self.screen.blit(pre_player_ready, (114, 200))
                self.screen.blit(player_ready, (500, 600))
            if self.ready_gamer_num == 2:
                pre_player_ready = pygame.image.load(r"source\ok.png")
                next_player_ready = pygame.image.load(r"source\ok.png")
                player_ready = pygame.image.load(r"source\ok.png")
                self.screen.blit(pre_player_ready, (114, 200))
                self.screen.blit(next_player_ready, (914, 200))
                self.screen.blit(player_ready, (500, 600))
                time.sleep(2)
                # 状态跳到抢地主
                self.status = "qdz"
            pygame.display.update()


class GameFrameThread(threading.Thread):
    def __init__(self, threadID, name, game_frame):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game_frame = game_frame

    def run(self):
        print("开始窗体线程：" + self.name)
        self.game_frame.main_paint_loop()
        print("退出线程：" + self.name)
