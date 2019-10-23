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
        self.button_rob = pygame.image.load(r".\source\button\rob.png")  # 抢地主按钮
        self.button_un_rob = pygame.image.load(r".\source\button\unrob.png")  # 不抢按钮
        self.clock_image = pygame.image.load(r"source\clock.png")  # 闹钟图片
        self.boss_poker_back_image = pygame.image.load(r"source\pokerBack.png")  # 地主牌（牌背）
        self.screen = pygame.display.set_mode([1133, 754])
        self.screen.blit(self.back_ground, (0, 0))
        self.position = []
        self.gamer_time = 0
        pygame.display.set_caption("斗地主")
        pygame.init()

    def draw_back_ground(self):
        self.screen.blit(self.back_ground, (0, 0))

    def draw_self_pokers(self):
        start_position = (1133 - ((len(self.client.pokers) - 1) * 50 + 105)) // 2
        for i in range(len(self.client.pokers)):
            temp_path = "source\pokers2\\" + self.client.pokers[i].card_type + self.client.pokers[i].card_text + ".jpg"
            poker_image = pygame.image.load(r"" + temp_path)
            self.screen.blit(poker_image, (i * 50 + start_position, 550))

    def draw_others_pokers(self):
        temp_text = str(self.client.pokers_size[(self.client.index + 2) % 3])
        pre_font = pygame.font.Font(None, 60).render(r"" + temp_text, True, (75, 175, 145))
        pre_image = pygame.image.load(r"source\pokerBack.png")
        pre_image.blit(pre_font, (30, 50))
        self.screen.blit(pre_image, (114, 200))  # 牌背的位置
        temp_text = str(self.client.pokers_size[(self.client.index + 1) % 3])
        next_font = pygame.font.Font(None, 60).render(r"" + temp_text, True, (75, 175, 145))
        next_image = pygame.image.load(r"source\pokerBack.png")
        next_image.blit(next_font, (30, 50))
        self.screen.blit(next_image, (914, 200))  # 牌背的位置

    def draw_clock(self):
        # 闹钟位置
        if self.client.now_gamer == "me":
            clock_image_me = pygame.image.load(r"source\clock.png")
            me_font = pygame.font.Font(None, 60).render(str(self.gamer_time), True, (75, 175, 145))
            clock_image_me.blit(me_font, (18, 30))
            self.screen.blit(clock_image_me, (150, 450))
        elif self.client.now_gamer == "next":
            clock_image_next = pygame.image.load(r"source\clock.png")
            next_font = pygame.font.Font(None, 60).render(str(self.gamer_time), True, (75, 175, 145))
            clock_image_next.blit(next_font, (18, 30))
            self.screen.blit(clock_image_next, (800, 200))
        elif self.client.now_gamer == "pre":
            clock_image_pre = pygame.image.load(r"source\clock.png")
            pre_font = pygame.font.Font(None, 60).render(str(self.gamer_time), True, (75, 175, 145))
            clock_image_pre.blit(pre_font, (18, 30))
            self.screen.blit(clock_image_pre, (250, 200))

    def draw_back_boss_poker(self):
        start_position = (1133 - (3 * 105 + 150)) // 2
        for i in range(3):
            self.screen.blit(self.boss_poker_back_image, (i * 150 + start_position, 0))

    def main_paint_loop(self):
        while True:
            now_time = time.time()
            self.gamer_time = self.client.max_time - int(now_time - self.client.last_time)
            if self.gamer_time < 0:
                self.gamer_time = 0
                if now_time < self.client.last_time:
                    self.gamer_time = self.client.max_time
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.client.status == "wait":
                self.wait()
            elif self.client.status == "fp":
                self.fp()
            elif self.client.status == "qdz":
                self.qdz()
            pygame.display.update()

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
        self.draw_self_pokers()
        # todo
        self.draw_others_pokers()

    def qdz(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if self.client.now_gamer == "me":
                if event.type == MOUSEBUTTONDOWN:
                    # 获取鼠标点击的区域
                    self.position = pygame.mouse.get_pos()
                    print("x:", self.position[0], "y", self.position[1])
                    if (350 < self.position[0] < 450) and (450 < self.position[1] < 510):
                        self.client.send("y")
                    elif (500 < self.position[0] < 600) and (450 < self.position[1] < 510):
                        self.client.send("n")
                    break
        self.draw_back_ground()
        if self.client.now_gamer == "me":
            self.screen.blit(self.button_rob, (350, 450))
            self.screen.blit(self.button_un_rob, (500, 450))
        self.draw_clock()
        self.draw_self_pokers()
        self.draw_others_pokers()
        self.draw_back_boss_poker()
        if self.gamer_time <= 0:
            self.client.send("n")


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
