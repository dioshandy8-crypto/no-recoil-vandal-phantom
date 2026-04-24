import cv2
import numpy as np
import mss
import win32api
import win32con
import keyboard
import time

# --- KONFIGURASI SENJATA ---
VANDAL_SETTINGS = {"speed": 3, "delay": 0.035} 
PHANTOM_SETTINGS = {"speed": 2, "delay": 0.020}

current_weapon = "VANDAL"
active_config = VANDAL_SETTINGS

# --- KONFIGURASI WARNA (PURPLE TRITANOPIA) ---
LOWER_PURPLE = np.array([140, 110, 150]) 
UPPER_PURPLE = np.array([160, 255, 255])
ZONE = 50 

sct = mss.mss()
screen_w = win32api.GetSystemMetrics(0)
screen_h = win32api.GetSystemMetrics(1)

region = {
    "top": int(screen_h / 2 - ZONE / 2),
    "left": int(screen_w / 2 - ZONE / 2),
    "width": ZONE,
    "height": ZONE
}

def is_enemy_detected():
    img = np.array(sct.grab(region))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_PURPLE, UPPER_PURPLE)
    return cv2.countNonZero(mask) > 5

print("="*30)
print(f"VALORANT RECOIL ASSIST AKTIF")
print(f"MODE: {current_weapon}")
print("F1: VANDAL | F2: PHANTOM | END: EXIT")
print("="*30)

try:
    while True:
        if keyboard.is_pressed('f1'):
            current_weapon, active_config = "VANDAL", VANDAL_SETTINGS
            print(f"[!] Switched to {current_weapon}")
            time.sleep(0.3)

        if keyboard.is_pressed('f2'):
            current_weapon, active_config = "PHANTOM", PHANTOM_SETTINGS
            print(f"[!] Switched to {current_weapon}")
            time.sleep(0.3)

        if win32api.GetAsyncKeyState(0x01) < 0:
            if is_enemy_detected():
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, active_config["speed"], 0, 0)
                time.sleep(active_config["delay"])
        
        if keyboard.is_pressed('end'):
            break
        time.sleep(0.001)
except Exception as e:
    print(f"Error: {e}")
