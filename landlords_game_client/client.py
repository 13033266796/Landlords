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
