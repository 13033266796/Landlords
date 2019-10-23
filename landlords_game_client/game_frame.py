import pygame
import sys
import time
import threading
from pygame.locals import *


class GameFrame:
    def __init__(self, client):
        self.client = client
        self.back_ground = pygame.image.load(r".\\source\\background\\backGround_1.png")
        self.player_ready = pygame.image.load(r"source\ok.png")
        self.screen = pygame.display.set_mode([1133, 754])
        self.screen.blit(self.back_ground, (0, 0))
        pygame.display.set_caption("斗地主")
        pygame.init()

    def main_paint_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.client.status == "wait":
                self.wait()
            elif self.client.status == "fp":
                self.fp()
            pygame.display.update()
            # 控制帧率
            time.sleep(1 / 60)

    def wait(self):
        self.screen.blit(self.back_ground, (0, 0))
        if self.client.ready_gamer_num == 1:
            self.screen.blit(self.player_ready, (500, 600))
        elif self.client.ready_gamer_num == 2:
            self.screen.blit(self.player_ready, (114, 200))
            self.screen.blit(self.player_ready, (500, 600))
        elif self.client.ready_gamer_num == 3:
            self.screen.blit(self.player_ready, (114, 200))
            self.screen.blit(self.player_ready, (914, 200))
            self.screen.blit(self.player_ready, (500, 600))

    def fp(self):
        start_position = (1133 - ((len(self.client.pokers) - 1) * 50 + 105)) // 2
        for i in range(len(self.client.pokers)):
            temp_path = "source\pokers2\\"+self.client.pokers[i].card_type+self.client.pokers[i].card_text+".jpg"
            poker_image = pygame.image.load(r""+temp_path)
            self.screen.blit(poker_image, (i * 50 + start_position, 550))
        # todo
        pre_font = pygame.font.Font(None, 60).render("17", True, (75, 175, 145))
        pre_image = pygame.image.load(r"source\pokerBack.png")
        pre_image.blit(pre_font, (30, 50))
        self.screen.blit(pre_image, (114, 200))  # 牌背的位置
        next_font = pygame.font.Font(None, 60).render("17", True, (75, 175, 145))
        next_image = pygame.image.load(r"source\pokerBack.png")
        next_image.blit(next_font, (30, 50))
        self.screen.blit(next_image, (914, 200))  # 牌背的位置


class GameFrameThread(threading.Thread):
    def __init__(self, threadID, name, game_frame_):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game_frame_ = game_frame_

    def run(self):
        print("开始窗体线程：" + self.name)
        self.game_frame_.main_paint_loop()
        print("退出线程：" + self.name)


if __name__ == "__main__":
    game_frame = GameFrame()
    # paint_thread = GameFrameThread(3, "paint_thread", game_frame)
    # paint_thread.start()
    game_frame.main_paint_loop()
