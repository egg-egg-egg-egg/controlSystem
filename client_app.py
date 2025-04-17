import socketio
import time
import base64
from enum import Enum
from client.screen_capture import ScreenCapture
import cv2
import numpy as np
import threading

class CommandType(Enum):
    SCREENSHOT = 1

class SocketIOClient:
    def __init__(self, server_url="http://127.0.0.1:8848", ping_interval=5000):
        self.sio = socketio.Client()
        self.screen_capture = ScreenCapture(70)
        self.server_url = server_url
        self.streaming = False
        # 注册事件处理器
        self.sio.on('connect', self._on_connect)
        self.sio.on('disconnect', self._on_disconnect)
        self.sio.on('ack', self._on_ack)
        self.sio.on('start_streaming', self._start_streaming)
        self.sio.on('stop_streaming', self._stop_streaming)

        # 添加心跳定时器
        self.ping_interval = ping_interval  # 5秒
        self.sio.on('custom-pong', self._on_pong)
        self.sio.on('custom-ping', self._start_heartbeat)
        
        # 视频流设置
        self.streaming = False

    def conniect(self):
        """连接到服务器"""
        server_url = self.server_url
        try:
            self.sio.connect(server_url)
        except Exception as e:
            print(f"连接异常: {e}")
        # finally:
        #     self.sio.disconnect()

    def _start_heartbeat(self):
        def send_ping():
            self.sio.emit('custom-ping', {'ts': time.time()})
        threading.Timer(self.ping_interval/1000, send_ping).start()

    def _on_pong(self, data):
        print(f"服务端心跳响应延迟: {time.time() - data['ts']}秒")
        self._start_heartbeat()  # 递归触发
        
    def _on_connect(self):
        self.connection_time = time.time()  # 记录连接时间
        # 时间转换为可读格式
        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.connection_time))
        print(f"{readable_time} 成功连接服务端: {self.server_url}")

    def _on_disconnect(self):
        self.deconnection_time = time.time()  # 记录连接时间
        # 时间转换为可读格式
        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.deconnection_time))
        print(f"{readable_time} 与服务端断开连接: {self.server_url}")
        self._stop_streaming()

    def _on_ack(self, data):
        """接收服务端确认消息"""
        print(f"服务端确认接收: {data}")

    def _stop_streaming(self):
        if self.streaming:
            self.streaming = False
            print("停止发送屏幕截图流")
        else:
            print("未开始发送屏幕截图流")

    def _start_streaming(self):
        self.streaming = True
        print("开始发送屏幕截图流")
        # 启动视频流发送线程
        # threading.Thread(target=self._start_video_stream, args=(0.5,), daemon=True).start()
        self._start_video_stream(interval=1)


    def _start_video_stream(self, interval=1):
        """开始视频流发送"""
        
        def send_frame():
            
            frame = self.screen_capture.get_frame()
            print("发送屏幕截图")
            # 优化点：使用JPEG压缩减少数据量（网页1方案增强）
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, self.screen_capture.quality])
            
            encoded_frame = base64.b64encode(buffer).decode('utf-8')
            
            # 结构化数据包（网页6最佳实践）
            self.sio.emit('screenshot', {
                'type': CommandType.SCREENSHOT.name,
                'data': encoded_frame,
                'meta': {'width': frame.shape[1], 'height': frame.shape[0]}
            })
        # self.sio.connected and 
        while self.streaming:
            send_frame()
            
            time.sleep(interval)
        

if __name__ == "__main__":
    # 客户端完整调用示例
    client = SocketIOClient(server_url="http://127.0.0.1:8848")

    
    client.conniect()