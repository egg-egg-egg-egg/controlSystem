import pyautogui
from ctypes import windll

class InputController:
    def __init__(self):
        self.original_mouse_state = True
        self.original_keyboard_state = True

    def lock_input(self, lock=True):
        windll.user32.BlockInput(lock)
        
    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y)
    
    def send_keys(self, text):
        pyautogui.write(text)