import socket
import json
import time

HOST = 'localhost'
PORT = 9500
BUF = 1024
ADDR = (HOST, PORT)


class Server:
    def __init__(self):
        self.connection = []

    def wait_connect(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen(5)

        for index in range(3):
            print("等待第", index + 1, "个客户端连接...", sep="")
            conn, addr = server.accept()

            self.connection.append(conn)
            # 发送玩家标号
            conn.send(str(index).encode())
            for i in range(index + 1):
                self.send_json(i, "ready", str(index + 1))

            print("连接数:", index + 1, sep="")
            print("新连接地址：", addr)

    # 发送数据
    def send(self, index, data):
        time.sleep(0.1)
        self.connection[index].send(data.encode())
        # print(index, "发送", data)

    # json 组包
    def send_json(self, index, code, data=""):
        json_data = json.dumps({"code": code, "data": data})
        self.send(index, json_data)
        print(index, "发送Json:", json_data)

    # 接受数据
    def recv(self, index):
        data = self.connection[index].recv(BUF).decode()
        print(index, "接收", data)
        return data

    # json拆包
    def recv_json(self, index):
        json_data = json.loads(self.recv(index))
        print(index, "接收Json:", json_data)
        return json_data
