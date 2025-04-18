import socketio
import base64
import cv2
import numpy as np
from eventlet import wsgi, listen
# dataclass
from dataclasses import dataclass
from threading import Lock
import time

@dataclass
class ImageData:
    frame: np.ndarray
    width: int
    height: int

class ServerNetwork:
    def __init__(self, port=65432):
        self.sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        self.clients = {}  # {sid: ip}
        self.port = port
        self.callback = None

        # 注册事件监听
        self.sio.on('connect', self._handle_connect)
        self.sio.on('disconnect', self._handle_disconnect)
        self.sio.on('screenshot', self._handle_screenshot)  # 修改为专用事件
        self.sio.on('test', self._handle_test)

        # ... 保持原有初始化 ...
        self.current_frame = None
        # self.display_lock = Lock()
        # self._init_display_thread()  # 初始化显示线程

    def _handle_test(self, sid, data):
        """测试事件处理"""
        client_ip = self.clients.get(sid)
        print(f"收到来自 {client_ip} 的测试消息: {data}")
        self.sio.emit('ack', {'status': 'success'}, to=sid)

    def start_listening(self, callback):
        self.callback = callback
        wsgi.server(listen(('0.0.0.0', self.port)), self.app)

    def _handle_connect(self, sid, environ):
        client_ip = environ.get('REMOTE_ADDR')
        self.clients[sid] = client_ip
        print(f"客户端 {client_ip} 已连接")
        

    def _handle_disconnect(self, sid):
        client_ip = self.clients.pop(sid, None)
        print(f"客户端 {client_ip} 已断开连接")

    def _handle_screenshot(self, sid, data):
        """专门处理截图数据流[3,6](@ref)"""
        client_ip = self.clients.get(sid)
        if not self.callback:
            print("未注册回调函数，丢弃消息")
            return

        try:
            # 验证数据结构[6](@ref)
            if not isinstance(data, dict):
                raise ValueError("消息格式错误，需为字典类型")
            
            # 解析元数据和图像数据[6](@ref)
            encoded_data = data.get('data', '')
            meta: dict = data.get('meta', {})
            
            # Base64解码[3](@ref)
            img_bytes = base64.b64decode(encoded_data)
            
            # 转换为OpenCV格式[4](@ref)
            np_array = np.frombuffer(img_bytes, dtype=np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            
            if frame is None:
                raise ValueError("图像解码失败")

            # 更新显示帧
            # with self.display_lock:
            #     self.current_frame = frame
            
            # 不通过回调操作GUI线程，避免阻塞
            self.callback(client_ip, {
                "frame": frame,
                "width": meta.get('width', 0),
                "height": meta.get('height', 0)
            })

            # 发送确认响应[2](@ref)
            self.sio.emit('ack', {'status': 'success'}, to=sid)

        except Exception as e:
            print(f"处理 {client_ip} 截图失败: {str(e)}")
            self.sio.emit('ack', {'status': 'error', 'msg': str(e)}, to=sid)


    def _init_display_thread(self):
        """初始化独立显示线程"""
        import threading
        def display_loop():
            # cv2.namedWindow('Server Preview', cv2.WINDOW_NORMAL)
            # cv2.resizeWindow('Server Preview', 640, 480)
            # cv2.moveWindow('Server Preview', 1000, 100)
            
            while True:
                with self.display_lock:
                    if self.current_frame is not None:
                        cv2.imshow('Server Preview', self.current_frame)
                        # 关键优化：统一处理窗口事件
                        if cv2.waitKey(33) & 0xFF == 27:  # 按ESC退出
                            cv2.destroyAllWindows()
                            break
                time.sleep(0.03)  # 约30fps

        self.display_thread = threading.Thread(target=display_loop, daemon=True)
        self.display_thread.start()
if __name__ == "__main__":
    # 创建一个窗口
    
    # cv2.namedWindow('Server Preview', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Server Preview', 640, 480)
    # # 设置窗口位置到屏幕右上角
    # cv2.moveWindow('Server Preview', 1000, 100)

    # # 示例回调函数（显示图像）
    def display_callback(client_ip, img_data):
        print(f"收到来自 {client_ip} 的图像: {img_data['width']}x{img_data['height']}")
        # 显示图像
        # cv2.imshow('Server Preview', img_data['frame'])
        # # 等待1毫秒，保持窗口响应
        # cv2.waitKey(1)

    server = ServerNetwork(port=8848)
    # server.start_listening(callback=display_callback)
    callback = display_callback
    server.start_listening(callback=callback)