from queue import Queue
from client import *
from game_frame import *
from client_gui import *


class BackgroundThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始背景线程：" + self.name)
        main_loop()
        print("退出线程：" + self.name)


class MsgThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始消息线程：" + self.name)
        main_msg_loop()
        print("退出线程：" + self.name)


def main_msg_loop():
    while True:
        data_ = client.recv_json()
        for data in data_:
            msg_queue.put(data)


def main_loop():
    while True:
        if msg_queue.empty():
            continue
        dict_data = msg_queue.get()
        code = dict_data["code"]
        data = dict_data["data"]
        if code == "close":
            break
        elif code == "ready":
            client.ready_gamer_num = int(data)
            print(str(data) + "个玩家已连接")
        elif code == "fp":
            print("收到牌：")
            client.pokers = PokerUtil.get_pokers_from_data(data)
            # 客户端转到发牌阶段
            client.status = "fp"
            # client.show_poker()
        # 抢地主的状态
        elif code == "qdz":
            client.last_time = time.time()
            print("到我抢地主了")
            client.now_gamer = "me"
            client.qdz_result = "_"
            client.status = "qdz"
            # 允许发送消息
            client.send_flag = True
        elif code == "sqdz":
            if data == "":
                client.last_time = time.time()
                client.now_gamer = "pre"
                print("现在轮到上家抢地主")
                client.status = "qdz"
            elif data == "by":
                client.qdz_pre_result = "n"
                print("上家不要地主")
            elif data == "qdz":
                client.qdz_pre_result = "y"
                print("上家抢地主")
        elif code == "xqdz":
            if data == "":
                client.last_time = time.time()
                client.now_gamer = "next"
                print("现在轮到下家抢地主")
                client.status = "qdz"
            elif data == "by":
                client.qdz_next_result = "n"
                print("下家不要地主")
            elif data == "qdz":
                client.qdz_next_result = "y"
                print("下家抢地主")
        # 指定地主
        elif code == "dz":
            print("我是地主")
            print("地主牌：", data)
            client.dz_pokers = list(PokerUtil.get_pokers_from_data(data))
            client.show_dz_poker()
            for poker in client.dz_pokers:
                client.pokers.append(poker)
            PokerUtil.sort_pokers(client.pokers, True)
            print()
            print("我的牌有：", len(client.pokers))
            client.show_poker()
        # 指定农民
        elif code == "nm":
            print("我是农民")
            print("地主牌：", data)
            client.dz_pokers = PokerUtil.get_pokers_from_data(data)
            client.show_dz_poker()
            print()
            client.show_poker()
        # 重新发牌
        elif code == "resend":
            client.pokers.clear()
            # pokers = list(PokerUtil.get_pokers_from_data(data))
        # 传输地主序号
        elif code == "dz_index":
            client.last_time = time.time()
            client.dz_index = data
            client.pokers_size[client.dz_index] = 20
            if client.dz_index == client.index:
                client.now_gamer = "me"
            elif client.dz_index == (client.index + 1) % 3:
                client.now_gamer = "next"
            else:
                client.now_gamer = "pre"
            client.status = "cp"
        # 出牌
        elif code == "cp":
            client.last_time = time.time()
            client.show_pokers_lock.acquire()
            client.pre_pokers = PokerUtil.get_pokers_from_data(data)
            client.show_pokers.clear()
            client.show_pokers_lock.release()
            client.send_poker_flag = "_"
            client.status = "cp"
            client.now_gamer = "me"
            client.send_flag = True
        # 上家出牌
        elif code == "scp":
            client.status = "cp"
            client.show_pokers_pre_lock.acquire()
            if data == "cp":
                client.last_time = time.time()
                client.now_gamer = "pre"
                client.show_pokers_pre.clear()
            # 过牌
            elif data == "gp":
                print("上家过牌")
                client.show_pokers_pre.clear()
            else:
                client.show_pokers_pre = PokerUtil.get_pokers_from_data(data)
                client.pokers_size[(client.index + 2) % 3] = client.pokers_size[(client.index + 2) % 3] - len(
                    client.show_pokers_pre)
            client.show_pokers_pre_lock.release()
        # 下家出牌
        elif code == "xcp":
            client.status = "cp"
            client.show_pokers_next_lock.acquire()
            if data == "cp":
                client.last_time = time.time()

                client.show_pokers_next.clear()
                client.now_gamer = "next"
            elif data == "gp":
                print("下家过牌")
                client.show_pokers_next.clear()
            else:
                client.show_pokers_next = PokerUtil.get_pokers_from_data(data)
                client.pokers_size[(client.index + 1) % 3] = client.pokers_size[(client.index + 1) % 3] - len(
                    client.show_pokers_next)
            client.show_pokers_next_lock.release()
        # 有玩家已经出完牌
        elif code == "win":
            client.status = "win"
            if data == "dz":
                print("地主胜利")
            if data == "nm":
                print("农民胜利")
            client.win = data
            break


if __name__ == "__main__":
    ip = ""
    while ip == "":
        ip = input_ip()
    client = Client(ip)
    msg_queue = Queue()
    game_frame = GameFrame(client)
    msg_thread = MsgThread(1, "msg_thread")
    background_thread = BackgroundThread(2, "background_thread")
    msg_thread.start()
    background_thread.start()
    game_frame.main_paint_loop()
