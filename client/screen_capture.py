from mss import mss
import cv2
import numpy as np

class ScreenCapture:
    def __init__(self, quality=50):
        self.sct = mss()
        self.quality = quality

    def get_frame(self):
        monitor = self.sct.monitors[1]
        img = self.sct.grab(monitor)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        _, jpeg = cv2.imencode('.jpg', frame, 
                              [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
        return jpeg.tobytes()