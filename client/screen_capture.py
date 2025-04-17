from mss import mss
import cv2
import numpy as np
from shared.protocol import create_command, CommandType

class ScreenCapture:
    def __init__(self, quality=50):
        self.quality = quality
        self._monitor = None  # 延迟初始化

    def get_frame(self):
        with mss() as sct:  # 每次捕获自动释放资源
            if not self._monitor:
                self._monitor = sct.monitors[1]
            img = sct.grab(self._monitor)
            return cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

    def set_quality(self, quality):
        """设置图像质量"""
        self.quality = quality

def send_frame(network_client, frame):
    command = create_command(CommandType.SCREENSHOT, {"data": frame})
    network_client.send(command)


if __name__ == "__main__":
    # 示例用法
    screen_capture = ScreenCapture()
    frame = screen_capture.get_frame()
    import json
    # 假设 network_client 是一个已连接的网络客户端实例
    # send_frame(network_client, frame)
    # 这里可以添加代码来处理发送帧到服务器的逻辑
    frame_data = frame.tobytes()
    command = create_command(CommandType.SCREENSHOT, {"data": frame_data})
    json_data = json.loads(command.decode())

    # 解析json数据并显示图片
    data = json_data["data"]
    frame = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()