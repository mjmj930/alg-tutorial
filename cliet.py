# manager.py（Socket客户端管理）
import socket
import threading
import time
from queue import Queue, Empty

from construct import StreamError


class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.msg_queues = {
            'heartbeat': Queue(),
            'control': Queue(),  # 控制类消息（握手/订阅/路测开关）
            'indicator': Queue()  # 指标数据消息
        }
        self.running = False
        self.connection_status = {
            'handshaked': False,
            'subscribed': False,
            'roadtest_opened': False
        }
        self.send_lock = threading.Lock()
        self.heartbeat_manager = None
        self.control_manager = None
        self.indicator_processor = None

    def connect(self):
        """建立连接并启动接收线程"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.running = True

        # 启动接收主线程
        threading.Thread(target=self._recv_dispatcher, daemon=True).start()

        # 启动心跳处理线程
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_manager)
        self.heartbeat_thread.start()

        # 启动控制管理线程
        self.control_manager = threading.Thread(target=self._control_handler)
        self.control_manager.start()

        # 启动指标处理线程
        self.indicator_processor = threading.Thread(target=self._indicator_handler)
        self.indicator_processor.start()

        # 初始化握手
        self._send_ctrl_msg(build_handshake())

    def _recv_dispatcher(self):
        """接收分发主线程"""
        buffer = b''
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    raise ConnectionError("Connection closed by peer")

                buffer += data
                while len(buffer) >= 4:
                    # 解析消息头
                    header = msg_header.parse(buffer[:4])
                    if header.magic != 0xABCD:
                        buffer = buffer[4:]  # 跳过错误头
                        continue

                    total_length = header.length + 4
                    if len(buffer) < total_length:
                        break  # 等待完整消息

                    # 提取完整消息
                    full_msg = buffer[:total_length]
                    buffer = buffer[total_length:]

                    # 解析消息ID
                    msgid = int.from_bytes(full_msg[4:8], 'big')
                    body = full_msg[8:4 + header.length]

                    # 消息路由
                    if msgid in (0x0003, 0x0004):  # 心跳响应
                        self.msg_queues['heartbeat'].put((msgid, body))
                    elif msgid in (0x0001, 0x0002, 0x0005, 0x0006):  # 控制类消息
                        self.msg_queues['control'].put((msgid, body))
                    else:  # 指标数据消息
                        self.msg_queues['indicator'].put((msgid, body))

            except Exception as e:
                print(f"Connection error: {e}")
                self._reconnect()

    def _heartbeat_handler(self):
        """心跳处理线程（独立循环）"""
        last_send = 0
        while self.running:
            try:
                # 定时发送心跳
                if time.time() - last_send > 15:
                    with self.send_lock:
                        self.sock.sendall(build_heartbeat())
                    last_send = time.time()

                # 处理心跳响应（带超时）
                try:
                    msgid, body = self.msg_queues['heartbeat'].get(timeout=20)
                    if msgid == 0x0003:
                        resp = heartbeat_resp.parse(body)
                        print(f"Heartbeat ACK: {resp.status}")
                except Empty:
                    print("Heartbeat timeout!")
                    self._reconnect()

                time.sleep(1)
            except Exception as e:
                print(f"Heartbeat error: {e}")

    def _control_handler(self):
        """控制管理线程（握手/订阅/路测开关）"""
        ctrl_handlers = {
            0x0001: self._handle_handshake,
            0x0002: self._handle_subscribe,
            0x0005: self._handle_roadtest
        }

        while self.running:
            try:
                msgid, body = self.msg_queues['control'].get(timeout=1)
                handler = ctrl_handlers.get(msgid)
                if handler:
                    handler(body)
            except Empty:
                self._check_status_progress()

    def _indicator_handler(self):
        """指标数据处理线程"""
        indicator_handlers = {
            0x1001: self._handle_indicator1,
            0x1002: self._handle_indicator2
        }

        while self.running:
            try:
                msgid, body = self.msg_queues['indicator'].get(timeout=1)
                handler = indicator_handlers.get(msgid)
                if handler:
                    handler(body)
            except Empty:
                continue

    def _handle_handshake(self, body):
        resp = handshake_resp.parse(body)
        if resp.result == 0:
            print("Handshake success!")
            self.connection_status['handshaked'] = True
            # 发送订阅请求
            self._send_subscribe_requests()


    def _send_subscribe_requests(self):
        """发送所有指标订阅请求"""
        subscriptions = [
            (1, b'param1'),  # 指标1
            (2, b'param2'),  # 指标2
            # ...其他指标
        ]
        for sub_id, params in subscriptions:
            self._send_ctrl_msg(build_subscribe(sub_id, params))

    def _handle_subscribe(self, body):
        resp = subscribe_resp.parse(body)
        if resp.status == 0:
            print("Subscribe success!")
            if not self.connection_status['subscribed']:
                self.connection_status['subscribed'] = True
                # 发送路测开关请求
                self._send_ctrl_msg(build_roadtest_switch(1))  # 1=开启


    def _handle_roadtest(self, body):
        resp = roadtest_resp.parse(body)
        if resp.status == 0:
            print("Roadtest opened!")
            self.connection_status['roadtest_opened'] = True

    def _check_status_progress(self):
        """状态机检查"""
        if self.connection_status['handshaked'] and not self.connection_status['subscribed']:
            self._send_subscribe_requests()
        elif self.connection_status['subscribed'] and not self.connection_status['roadtest_opened']:
            self._send_ctrl_msg(build_roadtest_switch(1))

    def _send_ctrl_msg(self, data):
        """发送控制类消息（线程安全）"""
        with self.send_lock:
            self.sock.sendall(data)

    def _reconnect(self):
        """重连机制"""
        self.close()
        print("Reconnecting...")
        time.sleep(3)
        try:
            self.connect()
        except Exception as e:
            print(f"Reconnect failed: {e}")

    def close(self):
        """关闭连接"""
        self.running = False
        if self.sock:
            self.sock.close()
        # 重置连接状态
        for k in self.connection_status:
            self.connection_status[k] = False
        print("Connection closed")


# 补充结构定义示例
roadtest_resp = Struct(
    "status" / Int32ub  # 0-成功
)

# 使用示例
if __name__ == "__main__":
    client = SocketClient("localhost", 9000)
    client.connect()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()
