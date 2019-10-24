import threading
from gamer.gamer import *
from poker.poker import *
from server.server import *
from server_view import *


class GameLogic:
    def __init__(self):
        self.gamers = []
        self.server = Server()
        self.server.wait_connect()
        self.poker_manager = PokerManager()
        self.init_gamer()
        # 谁是地主
        self.dz_index = -1
        # 重新发牌次数
        self.resend_num = 0
        self.qdz_flags = []
        # 谁最先抢
        self.point = random.randint(0, 2)

    def init_gamer(self):
        for num in range(3):
            gamer = Gamer()
            self.gamers.append(gamer)

    def send_poker(self, resend_flag=False):
        if resend_flag:
            self.poker_manager = PokerManager()
            self.gamers.clear()
            self.init_gamer()
            for i in range(3):
                self.server.send_json(i, "resend_poker")
        # 发牌
        for i in range(3):
            self.poker_manager.send_card(self.gamers[i])
        # 传输发牌结果
        for i in range(3):
            self.server.send_json(i, "fp", PokerUtil.encoder_poker(self.gamers[i].pokers))

    def qdz(self):
        # 抢地主
        for index in range(3):
            gamer_index = (self.point + index) % 3
            self.server.send_json(gamer_index, "qdz")
            self.server.send_json((gamer_index + 1) % 3, "sqdz")
            self.server.send_json((gamer_index + 2) % 3, "xqdz")
            if self.server.recv(gamer_index) == "y":
                self.qdz_flags.append(str(gamer_index))
                self.server.send_json((gamer_index + 1) % 3, "sqdz", "qdz")
                self.server.send_json((gamer_index + 2) % 3, "xqdz", "qdz")
            else:
                self.server.send_json((gamer_index + 1) % 3, "sqdz", "by")
                self.server.send_json((gamer_index + 2) % 3, "xqdz", "by")
        # 三个都不抢，重新发牌
        if len(self.qdz_flags) == 0:
            self.resend_num += 1
            if self.resend_num < 3:
                self.send_poker(True)
                self.qdz()
            # 三轮没人抢地主
            else:
                self.dz_index = self.point
                self.appoint_dz()
                return 1
        # 有一个人抢了地主
        elif len(self.qdz_flags) == 1:
            self.dz_index = int(self.qdz_flags[0])
            self.appoint_dz()
        # 有两个人以上抢了地主
        else:
            for index in self.qdz_flags:
                self.server.send_json(int(index), "qdz")
                self.server.send_json((int(index) + 1) % 3, "sqdz")
                self.server.send_json((int(index) + 2) % 3, "xqdz")
                # 有人抢地主
                if self.server.recv(int(index)) == "y":
                    self.dz_index = int(index)
                    self.appoint_dz()
                    return 1
            # 没人抢地主，默认第一个抢地主的玩家为地主
            self.dz_index = int(self.qdz_flags[0])
            self.appoint_dz()

    def appoint_dz(self):
        cards = self.poker_manager.get_three_cards()
        for index in range(3):
            if int(self.dz_index) == int(index):
                print("地主是：", index)
                # 发牌给地主
                for poker in cards:
                    self.gamers[index].pokers.append(poker)
                # 指定身份
                self.server.send_json(index, "dz", PokerUtil.encoder_poker(cards))
                self.gamers[int(self.dz_index)].set_rule("dz")
            else:
                print("农民是：", index)
                self.server.send_json(index, "nm", PokerUtil.encoder_poker(cards))
                self.gamers[index].set_rule("nm")
            self.server.send_json(index, "dz_index", self.dz_index)

    def cp(self):
        next_gamer = self.dz_index
        b_pokers = ""
        b_pokers_gamer = -1
        while not self.win():
            # 已经过来了一轮，没人出牌
            if b_pokers_gamer == next_gamer:
                b_pokers = ""
            self.server.send_json(next_gamer, "cp", b_pokers)
            self.server.send_json((next_gamer + 1) % 3, "scp", "cp")
            self.server.send_json((next_gamer + 2) % 3, "xcp", "cp")
            poker_data = self.server.recv_json(next_gamer)
            print(next_gamer, "玩家出牌", poker_data)
            # 玩家出牌
            if poker_data["code"] == "cp":
                b_pokers = poker_data["data"]
                self.gamers[next_gamer].remove_pokers(PokerUtil.get_pokers_from_data(b_pokers))
                self.server.send_json((next_gamer + 1) % 3, "scp", b_pokers)
                self.server.send_json((next_gamer + 2) % 3, "xcp", b_pokers)
                b_pokers_gamer = next_gamer
            # 玩家过牌
            else:
                self.server.send_json((next_gamer + 1) % 3, "scp", "gp")
                self.server.send_json((next_gamer + 2) % 3, "xcp", "gp")
            next_gamer = (next_gamer + 1) % 3

    # 判断有玩家是否出完牌
    def win(self):
        for i in range(3):
            print(i, "玩家剩余", len(self.gamers[i].pokers))
            if len(self.gamers[i].pokers) == 0:
                self.server.send_json(i, "win", self.gamers[i].rule)
                self.server.send_json((i + 1) % 3, "win", self.gamers[i].rule)
                self.server.send_json((i + 2) % 3, "win", self.gamers[i].rule)
                return True
        else:
            return False


def server_main():
    game = GameLogic()
    game.init_gamer()
    game.send_poker()
    game.qdz()
    game.cp()


class ServerThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始服务器线程：" + self.name)
        server_main()
        print("退出线程：" + self.name)


if __name__ == "__main__":
    server_thread = ServerThread(1, "server_thread")
    server_thread.start()
    server_ui()

