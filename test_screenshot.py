import cv2
import numpy as np
from client.screen_capture import ScreenCapture

def test_screenshot():
    # 初始化屏幕捕获
    screen_capture = ScreenCapture()

    # 捕获屏幕画面
    frame = screen_capture.get_frame()

    if frame is not None and isinstance(frame, np.ndarray):
        # 保存截图到本地
        output_path = "screenshot_test.jpg"
        cv2.imwrite(output_path, frame)  # 保存图片
        print(f"截图已成功保存到 {output_path}")

        # 显示截图
        cv2.imshow("Screenshot", frame)
        cv2.waitKey(0)  # 等待按键关闭窗口
        cv2.destroyAllWindows()
    else:
        print("未能成功捕获屏幕画面，frame 无效或不是 NumPy 数组")
        if frame is None:
            print("frame 为 None")
        else:
            print(f"frame 类型: {type(frame)}")

if __name__ == "__main__":
    test_screenshot()
