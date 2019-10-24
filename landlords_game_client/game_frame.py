import pygame
import sys
import time
import threading
from pygame.locals import *
from poker import *


class GameFrame:
    def __init__(self, client):
        self.client = client
        self.back_ground = pygame.image.load(r".\\source\\background\\backGround_1.png")
        self.player_ready = pygame.image.load(r"source\ok.png")
        self.button_rob = pygame.image.load(r".\source\button\rob.png")  # 抢地主按钮
        self.button_rob_a = pygame.image.load(r".\source\button\rob_a.png")  # 抢地主按下按钮
        self.button_un_rob = pygame.image.load(r".\source\button\unrob.png")  # 不抢按钮
        self.button_un_rob_a = pygame.image.load(r".\source\button\unrob_a.png")  # 不抢按下按钮
        self.button_send = pygame.image.load(r".\source\button\send.png")
        self.button_pass_send = pygame.image.load(r".\source\button\pass_send.png")
        self.button_send_d = pygame.image.load(r".\source\button\send_down.png")  # 按钮按下
        self.button_pass_send_d = pygame.image.load(r".\source\button\pass_send_down.png")  # 按钮按下
        self.clock_image = pygame.image.load(r"source\clock.png")  # 闹钟图片
        self.boss_poker_back_image = pygame.image.load(r"source\pokerBack.png")  # 地主牌（牌背）
        self.pass_image = pygame.image.load(r"source\pass_3.png")
        self.rob_boss_image = pygame.image.load(r"source\rob_boss.png")
        self.boss_image = pygame.image.load(r"source\boss.png")  # 地主标识
        self.boss_win_image = pygame.image.load(r"source\boss_win.png")
        self.farmer_win_image = pygame.image.load(r"source\farmer_win.png")
        self.screen = pygame.display.set_mode([1133, 754])
        self.screen.blit(self.back_ground, (0, 0))
        self.gamer_time = 0
        self.events = []
        pygame.display.set_caption("斗地主")
        pygame.init()
        self.back_ground_sound = pygame.mixer.Sound("source\MusicEx_Exciting.ogg")
        pygame.mixer.init()
        self.back_ground_sound.play(-1)

    def draw_back_ground(self):
        self.screen.blit(self.back_ground, (0, 0))

    def draw_qdz(self):
        if not self.client.qdz_result == "_" and not self.client.now_gamer == "me":
            if self.client.qdz_result == "y":
                self.screen.blit(self.rob_boss_image, (500, 400))
            elif self.client.qdz_result == "n":
                self.screen.blit(self.pass_image, (500, 400))
        if not self.client.qdz_next_result == "_" and not self.client.now_gamer == "next":
            if self.client.qdz_next_result == "y":
                self.screen.blit(self.rob_boss_image, (764, 200))
            elif self.client.qdz_next_result == "n":
                self.screen.blit(self.pass_image, (764, 200))
        if not self.client.qdz_pre_result == "_" and not self.client.now_gamer == "pre":
            if self.client.qdz_pre_result == "y":
                self.screen.blit(self.rob_boss_image, (250, 200))
            elif self.client.qdz_pre_result == "n":
                self.screen.blit(self.pass_image, (250, 200))

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
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == QUIT:
                    sys.exit()
            if self.client.status == "wait":
                self.wait()
            elif self.client.status == "fp":
                self.fp()
            elif self.client.status == "qdz":
                self.qdz()
            elif self.client.status == "cp":
                self.cp()
            elif self.client.status == "win":
                self.win()
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
        for event in self.events:
            if self.client.now_gamer == "me":
                if event.type == MOUSEBUTTONDOWN:
                    # 获取鼠标点击的区域
                    print("x:", event.pos[0], "y", event.pos[1])
                    if (350 < event.pos[0] < 450) and (450 < event.pos[1] < 510):
                        self.client.qdz_result = "y"
                    elif (500 < event.pos[0] < 600) and (450 < event.pos[1] < 510):
                        self.client.qdz_result = "n"
                    if not self.client.qdz_result == "_":
                        self.client.send(self.client.qdz_result)

        self.draw_back_ground()
        if self.client.now_gamer == "me":
            if self.client.qdz_result == "_":
                self.screen.blit(self.button_rob, (350, 450))
                self.screen.blit(self.button_un_rob, (500, 450))
            elif self.client.qdz_result == "y":
                self.screen.blit(self.button_rob_a, (350, 450))
                self.screen.blit(self.button_un_rob, (500, 450))
            elif self.client.qdz_result == "n":
                self.screen.blit(self.button_rob, (350, 450))
                self.screen.blit(self.button_un_rob_a, (500, 450))
        self.draw_qdz()
        self.draw_clock()
        self.draw_self_pokers()
        self.draw_others_pokers()
        self.draw_back_boss_poker()
        if self.gamer_time <= 0 and self.client.now_gamer == "me":
            self.client.send("n")

    def cp(self):
        start_position = (1133 - ((len(self.client.pokers) - 1) * 50 + 105)) // 2
        for event in self.events:
            if event.type == MOUSEBUTTONDOWN:
                # 获取鼠标点击的区域
                position = event.pos
                print(position[0], position[1])
                if self.client.now_gamer == "me":  # 出牌阶段 监听点击出牌按钮
                    if start_position < position[0] <= start_position + 50 * (
                            len(self.client.pokers) - 1) + 105 and 500 < position[1] <= 700:
                        for i in range(len(self.client.pokers)):
                            if start_position + i * 50 < position[0] and position[0] - (
                                    start_position + i * 50) < 50:  # (350,xxx)
                                if i in self.client.position_list:
                                    self.client.position_list.remove(i)
                                else:
                                    self.client.position_list.append(i)  # 获取选中牌的下标
                            else:
                                pass
                    elif (350 < position[0] < 473) and (420 < position[1] < 488):
                        if self.client.position_list:
                            flag = False
                            pokers_ = []
                            for i in self.client.position_list:
                                pokers_.append(self.client.pokers[i])
                            if not self.client.pre_pokers:
                                flag = PokerJudge.firstPoker(pokers_)
                            else:
                                flag = PokerLogic.comparePre(pokers_, self.client.pre_pokers)
                            # 判断是否可以吃牌
                            if flag:
                                self.client.send_cp_data(pokers_)
                                self.client.show_pokers = pokers_
                                self.client.send_poker_flag = "y"
                                self.client.position_list.clear()
                            # 吃不起
                            else:
                                self.client.position_list.clear()
                    elif (500 < position[0] < 623) and (420 < position[1] < 488):
                        self.client.send_cp_data("")
                        self.client.send_poker_flag = "n"
                        self.client.position_list.clear()  # 清空

        self.draw_back_ground()
        self.draw_clock()

        if self.client.now_gamer == "me" and self.client.send_poker_flag == "_":
            # if PokerLogic.isOvercomePrev(self.client.pokers, self.client.show_pokers_pre):
            self.screen.blit(self.button_send, (350, 420))  # 出牌阶段显示出牌按钮
            self.screen.blit(self.button_pass_send, (500, 420))  # 出牌阶段显示不出按钮
        elif self.client.now_gamer == "me" and self.client.send_poker_flag == "y":
            self.screen.blit(self.button_send_d, (350, 420))  # 出牌阶段显示出牌按钮
            self.screen.blit(self.button_pass_send, (500, 420))  # 出牌阶段显示不出按钮
        elif self.client.now_gamer == "me" and self.client.send_poker_flag == "n":
            self.screen.blit(self.button_send, (350, 420))  # 出牌阶段显示出牌按钮
            self.screen.blit(self.button_pass_send_d, (500, 420))  # 出牌阶段显示不出按钮

        self.client.show_pokers_next_lock.acquire()
        # 展示下家出牌
        if self.client.show_pokers_next:
            if len(self.client.show_pokers_next) <= 6:
                start_position_next = 789 - 20 * (len(self.client.show_pokers_next) - 1)
                for i in range(len(self.client.show_pokers_next)):
                    temp_path = self.client.show_pokers_next[i].card_type + self.client.show_pokers_next[i].card_text
                    poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                    self.screen.blit(poker_image, (i * 20 + start_position_next, 200))
            elif len(self.client.show_pokers_next) > 6:
                start_position_next = 789 - 20 * (6 - 1)
                for i in range(len(self.client.show_pokers_next)):
                    temp_path = self.client.show_pokers_next[i].card_type + self.client.show_pokers_next[i].card_text
                    poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                    if i <= 5:
                        self.screen.blit(poker_image, (i * 20 + start_position_next, 200))
                    elif 6 <= i <= 11:
                        self.screen.blit(poker_image, (start_position_next + 20 * (i - 6), 250))
                    elif 12 <= i <= 17:
                        self.screen.blit(poker_image, (start_position_next + 20 * (i - 12), 300))
                    else:
                        self.screen.blit(poker_image, (start_position_next + 20 * (i - 18), 350))
        self.client.show_pokers_next_lock.release()
        # 展示上家出牌
        if self.client.show_pokers_pre:
            if len(self.client.show_pokers_pre) <= 6:
                start_position_pre = 239
                for i in range(len(self.client.show_pokers_pre)):
                    temp_path = self.client.show_pokers_pre[i].card_type + self.client.show_pokers_pre[i].card_text
                    poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                    self.screen.blit(poker_image, (i * 20 + start_position_pre, 200))
            elif len(self.client.show_pokers_pre) > 6:
                start_position_pre = 239
                for i in range(len(self.client.show_pokers_pre)):
                    temp_path = self.client.show_pokers_pre[i].card_type + self.client.show_pokers_pre[i].card_text
                    poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                    if i <= 5:
                        self.screen.blit(poker_image, (i * 20 + start_position_pre, 200))
                    elif 6 <= i <= 11:
                        self.screen.blit(poker_image, (start_position_pre + 20 * (i - 6), 250))
                    elif 12 <= i <= 17:
                        self.screen.blit(poker_image, (start_position_pre + 20 * (i - 12), 300))
                    else:
                        self.screen.blit(poker_image, (start_position_pre + 20 * (i - 18), 350))

        # 展示本机出牌
        if self.client.show_pokers:
            PokerUtil.sort_pokers(self.client.show_pokers)
            startPositin_3 = (1133 - ((len(self.client.show_pokers) - 1) * 50 + 105)) // 2
            for i in range(len(self.client.show_pokers)):
                temp_path = self.client.show_pokers[i].card_type + self.client.show_pokers[i].card_text
                poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                self.screen.blit(poker_image, (i * 50 + startPositin_3, 380))

        for i in range(len(self.client.pokers)):
            if i in self.client.position_list:
                temp_path = self.client.pokers[i].card_type + self.client.pokers[i].card_text
                poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                self.screen.blit(poker_image, (i * 50 + start_position, 500))
            else:
                temp_path = self.client.pokers[i].card_type + self.client.pokers[i].card_text
                poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                self.screen.blit(poker_image, (i * 50 + start_position, 550))

        self.draw_others_pokers()

        # 绘制地主标志
        # 本人
        if self.client.dz_index == self.client.index:
            self.screen.blit(self.boss_image, (114, 500))
        # 下家
        elif self.client.dz_index == (self.client.index + 1) % 3:
            self.screen.blit(self.boss_image, (1050, 100))
        # 上家
        elif self.client.dz_index == (self.client.index + 2) % 3:
            self.screen.blit(self.boss_image, (50, 100))

        if self.client.dz_pokers:
            # 地主牌位置
            startPositin_2 = (1133 - (3 * 105 + 150)) // 2
            for i in range(3):
                temp_path = self.client.dz_pokers[i].card_type + self.client.dz_pokers[i].card_text
                boss_poker_image = pygame.image.load(r"source\\pokers2\\" + temp_path + ".jpg")
                self.screen.blit(boss_poker_image, (i * 150 + startPositin_2, 0))
        if self.gamer_time <= 0 and self.client.now_gamer == "me":
            self.client.send_cp_data("")
            self.client.send_poker_flag = "n"
            self.client.position_list.clear()  # 清空

    def win(self):
        if self.client.win == "dz":
            self.screen.blit(self.boss_win_image, (450, 300))  # 地主获胜
        elif self.client.win == "nm":
            self.screen.blit(self.farmer_win_image, (450, 300))  # 农民获胜


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
