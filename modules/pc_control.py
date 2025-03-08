import os
import pyautogui

def open_app(app_name):
    print(f"Opening {app_name}...")
    os.system(f"start {app_name}")

def close_app(app_name):
    print(f"Closing {app_name}...")
    pyautogui.hotkey("alt", "f4")