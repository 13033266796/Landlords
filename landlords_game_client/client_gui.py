import sys
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode([1133, 754])
backGround = pygame.image.load(r".\\source\\background\\backGround_1.png")  # 背景图
input_box_image = pygame.image.load(r"source\input_box.png")
button_ip = pygame.image.load(r"source\button_ip.png")
tip_font = pygame.font.SysFont("simhei", 30).render("请输入房间号：", True, (70, 130, 180))
dict_input = {K_0: "0", K_1: "1", K_2: "2", K_3: "3", K_4: "4", K_5: "5", K_6: "6", K_7: "7", K_8: "8", K_9: "9",
              K_PERIOD: "."}


def input_ip():
    str_ip = ""
    ip_font = pygame.font.SysFont("simhei", 30).render(str_ip, True, (70, 130, 180))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if 350 < event.pos[0] <472 and 400 < event.pos[0] < 463:
                    return str_ip
            if event.type == KEYDOWN:
                if event.key in dict_input.keys():
                    str_ip += dict_input[event.key]
                    ip_font = pygame.font.SysFont("simhei", 30).render(str_ip, True, (70, 130, 180))
                elif event.key == K_BACKSPACE:
                    str_ip = str_ip[0:-1]
                    ip_font = pygame.font.SysFont("simhei", 30).render(str_ip, True, (70, 130, 180))
                elif event.key == K_RETURN:
                    return str_ip
        screen.blit(backGround, (0, 0))
        input_box_image = pygame.image.load(r"source\input_box.png")
        input_box_image.blit(ip_font, (15, 15))
        screen.blit(input_box_image, (350, 300))
        screen.blit(button_ip, (350, 400))
        screen.blit(tip_font, (350, 250))
        pygame.display.update()


if __name__ == "__main__":
    input_ip()
