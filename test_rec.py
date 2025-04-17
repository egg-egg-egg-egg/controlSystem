from mss import mss
import cv2
import numpy as np
from shared.protocol import create_command, CommandType
from client.screen_capture import ScreenCapture  # 假设你有一个网络客户端类


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
    json_data = json.loads(command.decode("utf-8"))

    data:list = json_data["data"]["data"]
    np_data = np.array(data, dtype=np.uint8)
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
