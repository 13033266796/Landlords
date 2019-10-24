import socket
import json

from poker import *

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
        # 已经准备好的玩家数
        self.ready_gamer_num = 0
        # 是否抢地主
        self.qdz_result = "_"
        self.qdz_next_result = "_"
        self.qdz_pre_result = "_"
        # 回合最大时间
        self.max_time = 30
        # 回合开始时间
        self.last_time = 0
        # 是否可以发送消息
        self.send_flag = False
        self.now_gamer = ""
        # 被点起来的牌
        self.position_list = []
        self.send_poker_flag = "_"
        self.show_pokers = []  # 出的牌
        self.pre_pokers = []
        self.show_pokers_next = []  # 下家出的牌
        self.show_pokers_pre = []  # 上家出的牌

    # 发送数据
    def send(self, data_):
        if self.send_flag:
            self.socket_.send(data_.encode())
            print("发送数据", data_)
            # 发送完自动禁止发送下一条
            self.send_flag = False
        else:
            print("发送被禁止")

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

    def send_cp_data(self, pokers):
        if pokers is None or len(pokers) == 0:
            print("过牌")
            self.send_json("gp", "")
        else:
            self.pokers_size[self.index] = self.pokers_size[self.index] - len(pokers)
            for poker_ in pokers:
                self.pokers.remove(poker_)
            cp_data = PokerUtil.encode_pokers(pokers)
            print("出牌：", cp_data)
            self.send_json("cp", cp_data)
