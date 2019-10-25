import sys
import pygame
from server.server import get_host_ip
from pygame.locals import QUIT

pygame.init()
screen = pygame.display.set_mode([1133, 754])
backGround = pygame.image.load(r".\\source\\backGround_1.png")  # 背景图
show_ip = pygame.image.load(r"source\input_box.png")
show_port = pygame.image.load(r"source\input_box.png")
ip_font = pygame.font.SysFont("simhei", 45).render("IP:", True, (255, 48, 48))
port_font = pygame.font.SysFont("simhei", 45).render("Port:", True, (255, 48, 48))

HOST = get_host_ip()
Port = 9500

host_font = pygame.font.SysFont("simhei", 45).render(str(HOST), True, (255, 48, 48))
Port_font = pygame.font.SysFont("simhei", 45).render(str(Port), True, (255, 48, 48))


def server_ui():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        screen.blit(backGround, (0, 0))

        screen.blit(show_ip, (350, 200))
        screen.blit(ip_font, (250, 210))
        show_ip.blit(host_font, (15, 15))

        screen.blit(show_port, (350, 400))
        screen.blit(port_font, (200, 410))
        show_port.blit(Port_font, (15, 15))
        pygame.display.update()


if __name__ == "__main__":
    server_ui()
