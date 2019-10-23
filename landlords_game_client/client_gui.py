import pygame
import sys
from pygame.locals import *
import random
import os
import threading
import time

class Player(object):
    def __init__(self,screen,pokers =[],identity = False):
        self.screen = screen
        self.pokers = pokers
        self.pokers_duixiang = []
        self.identity = identity
        self.send_pokers_list =[]

    # 用所得数据生成扑克对象
    def get_poker_duixiang(self):
        self.pokers_duixiang = []
        for i in range(len(self.pokers)):
            value, type_poker, num = self.pokers[i].split(" ")
            # 图片名字获取
            name_image = type_poker + value
            # 创建poker对象并显示
            startPositin = (1133 - ((len(self.pokers) - 1) * 50 + 105)) // 2  # 计算牌开始的水平位置，使自己所有的牌居中
            poker = Poker(self.screen, i * 50 + startPositin, type_poker, value, num, str(name_image))
            self.pokers_duixiang.append(poker)

    # 显示自己的手牌
    def display(self):
        for poker in self.pokers_duixiang:
            poker.display()

    # 判断鼠标点击了哪张牌
    def judge_poker_in_mouse(self,position):
        # 判断是哪张牌被选中
        for poker in self.pokers_duixiang:
            # 非最小的牌 只能点击不重复的部分
            pass
            if (position[0] > poker.x and position[0] < poker.x + 50) and (
                    position[1] > poker.y and position[1] < poker.y + 188):
                if poker.statu == False:
                    poker.choosedStatu()  # 点击一张牌 成为选中状态
                else:
                    poker.unChoosedStatu()  # 再次点击 恢复未选中状态

    # 本机玩家出牌
    def send_pokers(self):
        i_list =[]
        self.send_pokers_list = []
        # 将选中的牌暂存，并记录下标以便删除手牌列表中的数据 实时更新手牌的数量和位置
        for i in range(len(self.pokers_duixiang)):
            if self.pokers_duixiang[i].statu == True:
                i_list.append(i)
                self.send_pokers_list.append(self.pokers_duixiang[i])
        for i in i_list[::-1]:
            self.pokers_duixiang.remove(self.pokers_duixiang[i])
            self.pokers.remove(self.pokers[i])

        list = []
        for poker in self.send_pokers_list:
            list.append(poker.value+" "+poker.type_poker+" "+poker.num)
        return list

    # 显示出的牌
    def show_send_pokers(self):
        start_position = (1133 - ((len(self.send_pokers_list) - 1) * 50 + 105)) // 2
        for i in range(len(self.send_pokers_list)):
            self.send_pokers_list[i].display_with_xy(i * 50 + start_position, 380)

class otherPlayer(object):
    def __init__(self, temp_screen, x, identity= False):
        self.x = x # 上家114  下家914
        self.pokers = []# 其他玩家出牌列表
        self.screen = temp_screen
        self.identity = identity
        self.num = 17
        self.image = pygame.image.load(r"source\pokerBack.png")
        self.font = pygame.font.Font(None, 60).render(str(self.num), True, (75, 175, 145))

    def confirmBoss(self):
        self.identity = True # 是地主
        self.num = 20

    def display(self):
        self.font = pygame.font.Font(None, 60).render(str(self.num), True, (75, 175, 145))
        self.image = pygame.image.load(r"source\pokerBack.png")
        self.image.blit(self.font, (30, 50))
        self.screen.blit(self.image, (self.x, 200)) #牌背的位置


    def show_send_pokers_pre(self, pokers):
        self.pokers_duixiang = []
        for i in range(len(pokers)):

            value, type_poker, num = pokers[i].split(" ")
            # 图片名字获取
            name_image = type_poker + value
            # 创建poker对象并显示
            # startPositin = (1133 - ((len(self.pokers) - 1) * 50 + 105)) // 2  # 计算牌开始的水平位置，使自己所有的牌居中
            poker = Poker(self.screen, 111111, type_poker, value, num, str(name_image))
            self.pokers_duixiang.append(poker)
            # 上家出牌布局
            if len(self.pokers_duixiang) > 0 and len(self.pokers_duixiang) <= 6:
                startposition = 239
                for i in range(len(self.pokers_duixiang)):
                    self.pokers_duixiang[i].display_with_xy(startposition + 20 * i, 200)
            elif len(self.pokers_duixiang) > 6:
                startposition = 239
                for i in range(len(self.pokers_duixiang)):
                    if i <= 5:
                        self.pokers_duixiang[i].display_with_xy(startposition + 20 * i, 200)
                    elif i >= 6 and i <= 11:
                        self.pokers_duixiang[i].display_with_xy(startposition + 20 * (i - 6), 250)
                    elif i >= 12 and i <= 17:
                        self.pokers_duixiang[i].display_with_xy(startposition + 20 * (i - 12), 300)
                    else:
                        self.pokers_duixiang[i].display_with_xy(startposition + 20 * (i - 18), 350)

    def show_send_pokers_next(self,pokers):
        self.pokers_duixiang = []
        for i in range(len(pokers)):
            value, type_poker, num = pokers[i].split(" ")
            # 图片名字获取
            name_image = type_poker + value
            # 创建poker对象并显示
            # startPositin = (1133 - ((len(self.pokers) - 1) * 50 + 105)) // 2  # 计算牌开始的水平位置，使自己所有的牌居中
            poker = Poker(self.screen, 111111, type_poker, value, num, str(name_image))
            # print(poker)
            self.pokers_duixiang.append(poker)
        #下家出牌布局
        if len(self.pokers_duixiang) > 0 and len(self.pokers_duixiang) <= 6 :
            startposition = 789 - 20*(len(self.pokers_duixiang)-1)
            for i in range(len(self.pokers_duixiang)):
                self.pokers_duixiang[i].display_with_xy(startposition+20*i,200)
        elif len(self.pokers_duixiang) >6 :
            startposition = 789 - 20 *( 6 - 1)
            for i in range(len(self.pokers_duixiang)):
                if i <= 5:
                    self.pokers_duixiang[i].display_with_xy(startposition + 20 * i, 200)
                elif i >= 6 and i <=11:
                    self.pokers_duixiang[i].display_with_xy(startposition + 20 * (i-6), 250)
                elif i >= 12 and i <= 17:
                    self.pokers_duixiang[i].display_with_xy(startposition + 20 * (i-12), 300)
                else:
                    self.pokers_duixiang[i].display_with_xy(startposition + 20 * (i-18), 350)

    def clearPokers(self):
        self.pokers_duixiang = []

class Poker(object):
    def __init__(self,temp_screen,x,type_poker,value,num,name_image,statu = False,y = 550):
        self.type_poker = type_poker
        self.x = x
        self.y = y
        self.num = num
        self.value = value
        self.statu = statu #纸牌的状态 是否选中 默认未选中
        self.screen = temp_screen
        path = ".\\source\\pokers2\\" + name_image + ".jpg"
        # self.image = pygame.image.load(r"C:\Users\92931\Desktop\poker2.png")
        self.image = pygame.image.load(path)


    def __str__(self):
        return "%s %s"%(self.type_poker,self.num)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
    def display_with_xy(self,x,y):
        self.screen.blit(self.image,(x,y))

    def choosedStatu(self):
        self.statu = True
        self.y = self.y - 50

    # 取消选中
    def unChoosedStatu(self):
        self.statu = False
        self.y = self.y + 50

class DiPai(object):
    def __init__(self,screen,pokers):
        self.pokers = pokers
        self.pokers_duixiang = []
        self.screen = screen
        self.unkonw = pygame.image.load(r"source\pokerBack.png")

    def get_poker_duixiang(self):
        for i in range(len(self.pokers)):
            value, type_poker, num = self.pokers[i].split(" ")
            # 图片名字获取
            name_image = type_poker + value
            # 创建poker对象并显示
            startPositin = (1133 - (3 * 105 + 150)) // 2  # 计算牌开始的水平位置，使自己所有的牌居中
            poker = Poker(self.screen, i * 150 + startPositin, type_poker, value,num, str(name_image),y=0)
            self.pokers_duixiang.append(poker)

    def display(self):
        if self.pokers_duixiang:
            for poker in self.pokers_duixiang:
                poker.display()
        else:# 未确认地主时的底牌
            startPositin = (1133 - (3 * 105 + 150)) // 2
            for i in range(3):
                self.screen.blit(self.unkonw,(i * 150 + startPositin,0))

mypokers = ['Q x 9','8 m 5','2 f 12','K f 10','8 f 5','4 t 1','A f 11','8 t 5','9 f 6','9 m 6','6 f 3','3 x 0','6 x 3','3 f 0','3 m 0','2 x 12','K t 10']
# 出牌指令
# flag = False
flag = True
# flag_for_qiang = False # 抢地主指令
flag_for_qiang = True

set_boss = False

def main():
    global flag
    global flag_for_qiang
    global set_boss
    pygame.init()
    screen = pygame.display.set_mode([1133, 754])
    pygame.display.set_caption("斗地主")
    backGround = pygame.image.load(r".\\source\\background\\backGround_1.png")  # 背景图
    screen.blit(backGround, (0, 0))  # 设置背景图

    # 创建本机玩家
    player = Player(screen, mypokers)
    player.get_poker_duixiang()
    player.display()
    # 创建上家
    pre_player = otherPlayer(screen, 114)  # 114 -> 上家牌堆水平位置x
    pre_player.display()
    # 创建下家
    next_player = otherPlayer(screen, 914)  # 914 -> 下家牌堆水平位置x
    next_player.display()
    # 创建底牌
    dipai = DiPai(screen, [])
    dipai.get_poker_duixiang()
    # 创建出牌按钮
    buttun_send = pygame.image.load(r".\source\button\send.png")

    # 创建抢地主和 不抢按钮
    buttun_rob = pygame.image.load(r".\source\button\rob.png")
    buttun_unrob = pygame.image.load(r".\source\button\unrob.png")

    # 抢地主阶段
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # 获取鼠标点击的区域
                position = pygame.mouse.get_pos()
                # print(position)
                if flag_for_qiang:
                    if (position[0] > 350 and position[0] < 450) and (position[1] > 450 and position[1] < 510):
                        print("抢地主")
                        flag_for_qiang = False

                    if (position[0] > 500 and position[0] < 600) and (position[1] > 450 and position[1] < 510):
                        print("不抢")
                        flag_for_qiang = False
                        pre_player.confirmBoss()
                        set_boss = True

        screen.blit(backGround, (0, 0))
        # 是否抢地主
        if flag_for_qiang:
            screen.blit(buttun_rob, (350, 450))
            screen.blit(buttun_unrob, (500, 450))
        if set_boss:
            break
        dipai.display()
        player.display()
        pre_player.display()
        next_player.display()
        pygame.display.flip()

    # 游戏阶段
    while True:

        # 退出程序

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # 获取鼠标点击的区域
                position = pygame.mouse.get_pos()
                player.judge_poker_in_mouse(position)
                if flag:  # 出牌阶段 监听点击出牌按钮
                    if (position[0] > 350 and position[0] < 530) and (position[1] > 420 and position[1] < 488):
                        send_pokers = player.send_pokers()  # 返回 牌对象（已出） 列表
                        player.get_poker_duixiang()
                        flag = False  # 结束出牌

        screen.blit(backGround, (0, 0))
        player.display()
        player.show_send_pokers()

        pre_player.display()

        next_player.display()
        next_player.show_send_pokers_pre(['8 m 5', '2 f 12', 'K f 10', '2 f 12', 'K f 10', '2 f 12'])  # 上家出牌
        next_player.show_send_pokers_next(['8 m 5', '2 f 12', 'K f 10', '2 f 12', 'K f 10', '2 f 12'])  # 下家出牌
        dipai.display()

        if flag:
            screen.blit(buttun_send, (350, 420))  # 出牌阶段显示出牌按钮

        # 更新界面
        pygame.display.flip()





if __name__ == "__main__":
    main()
