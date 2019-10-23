import socket
import json
import threading
import client_gui
import queue

from poker import *
from game_frame import *

HOST = 'localhost'
PORT = 9500
ADDR = (HOST, PORT)
BUF = 1024


class Client:
    def __init__(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.connect(ADDR)
        self.index = int(self.socket_.recv(BUF).decode())
        print("玩家序号", self.index)
        self.pokers = []
        self.dz_pokers = []
        self.dz_index = -1
        # 各家剩余牌量
        self.pokers_size = [17, 17, 17]
        self.status = "wait"

    # 发送数据
    def send(self, data_):
        self.socket_.send(data_.encode())
        print("发送数据", data_)

    # json 组包
    def send_json(self, code_, data_=None):
        if data_ is None:
            data_ = []
        self.send(json.dumps({"code": code_, "data": data_}))

    # 接受数据
    def recv(self):
        data_ = self.socket_.recv(BUF).decode()
        print("收到数据", data_, "长度：", len(data_), type(data_))
        if data_ is None or len(data_) == 0:
            print("服务端已断开")
            self.socket_.close()
            return json.dumps({"code": "close", "data": []})
        return data_

    # json拆包
    def recv_json(self):
        return json.loads(self.recv())

    def show_poker(self):
        for poker_ in self.pokers:
            print(poker_.encode())

    def show_dz_poker(self):
        for poker_ in self.dz_pokers:
            print(poker_.encode())

    def send_cp_data(self, cp_data):
        if cp_data is None or len(cp_data) == 0:
            print("过牌")
            self.send_json("gp", "")
        else:
            pokers_ = PokerUtil.get_pokers_from_data(cp_data)
            self.pokers_size[self.index] = self.pokers_size[self.index] - len(pokers_)
            for poker_ in pokers_:
                self.pokers.remove(poker_)
            print("出牌：", cp_data)
            self.send_json("cp", cp_data)


class BackgroundThread(threading.Thread):
    def __init__(self, threadID, name, client_, msg_queue_, game_frame_):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.client_ = client_
        self.msg_queue_ = msg_queue_
        self.game_frame_ = game_frame_

    def run(self):
        print("开始背景线程：" + self.name)
        main_loop(self.client_, self.msg_queue_, game_frame)
        print("退出线程：" + self.name)


class MsgThread(threading.Thread):
    def __init__(self, threadID, name, client_, msg_queue_):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.client_ = client_
        self.msg_queue_ = msg_queue_

    def run(self):
        print("开始消息线程：" + self.name)
        main_msg_loop(self.client_, self.msg_queue_)
        print("退出线程：" + self.name)


def main_msg_loop(client_, msg_queue_):
    while True:
        data_ = client_.recv_json()
        msg_queue_.put(data_)
        print("消息队列入队：", data_)


def main_loop(client_, msg_queue_, game_frame_):
    while True:
        if msg_queue_.empty():
            continue
        dict_data = msg_queue_.get()
        code = dict_data["code"]
        data = dict_data["data"]
        client.status = code
        if code == "close":
            break
        elif code == "ready":
            game_frame.ready_gamer_num = int(data)
            print(data, "玩家已连接")
        elif code == "fp":
            print("收到牌：")
            client_.pokers = PokerUtil.get_pokers_from_data(data)
            client_.show_poker()
        # 抢地主的状态
        elif code == "qdz":
            print("到我抢地主了")
            client_.send("n")
        elif code == "sqdz":
            if data == "":
                print("现在轮到上家抢地主")
            elif data == "by":
                print("上家不要地主")
            elif data == "qdz":
                print("上家抢地主")
        elif code == "xqdz":
            if data == "":
                print("现在轮到下家抢地主")
            elif data == "by":
                print("下家不要地主")
            elif data == "qdz":
                print("下家抢地主")
        # 指定地主
        elif code == "dz":
            print("我是地主")
            print("地主牌：", data)
            dz_pokers = list(PokerUtil.get_pokers_from_data(data))
            client_.show_dz_poker()
            for poker in dz_pokers:
                client_.pokers.append(poker)
            PokerUtil.sort_pokers(client_.pokers)
            print()
            print("我的牌有：", len(client_.pokers))
            client_.show_poker()
        # 指定农民
        elif code == "nm":
            print("我是农民")
            print("地主牌：", data)
            dz_pokers = PokerUtil.get_pokers_from_data(data)
            client_.show_dz_poker()
            print()
            client_.show_poker()
        # 重新发牌
        elif code == "resend":
            client_.pokers.clear()
            # pokers = list(PokerUtil.get_pokers_from_data(data))
        # 传输地主序号
        elif code == "dz_index":
            client_.dz_index = data
            client_.pokers_size[client_.dz_index] = 20
        # 出牌
        elif code == "cp":
            # todo 这里是玩家出牌数据
            cp_data = None
            if data == "":
                client_.send_cp_data(cp_data)
            else:
                pre_cards = PokerUtil.get_pokers_from_data(data)
                if PokerLogic.isOvercomePrev(client_.pokers, pre_cards):
                    if cp_data is not None:
                        # 判断是否可以吃牌
                        if PokerLogic.comparePre(PokerUtil.get_pokers_from_data(cp_data), pre_cards):
                            client_.send_cp_data(cp_data)
                    else:
                        client_.send_cp_data(cp_data)
                # todo 这里直接过了，需要修改
                else:
                    client_.send_cp_data(cp_data)
        # 上家出牌
        elif code == "scp":
            # 过牌
            if data == "gp":
                print("上家过牌")
            else:
                cards = PokerUtil.get_pokers_from_data(data)
                client_.pokers_size[(client_.index + 2) % 3] = client_.pokers_size[(client_.index + 2) % 3] - len(cards)
        # 下家出牌
        elif code == "xcp":
            if data == "gp":
                print("下家过牌")
            else:
                cards = PokerUtil.get_pokers_from_data(data)
                client_.pokers_size[(client_.index + 1) % 3] = client_.pokers_size[(client_.index + 1) % 3] - len(cards)
        # 有玩家已经出完牌
        elif code == "win":
            if data == "dz":
                print("地主胜利")
            if data == "nm":
                print("农民胜利")
            break


if __name__ == "__main__":
    client = Client()
    msg_queue = queue.Queue()
    game_frame = GameFrame()
    msg_thread = MsgThread(1, "msg_thread", client, msg_queue)
    background_thread = BackgroundThread(2, "background_thread", client, msg_queue,game_frame)
    paint_thread = GameFrameThread(3,"paint_thread", game_frame)
    msg_thread.start()
    background_thread.start()
    paint_thread.start()

    while True:
        pass
