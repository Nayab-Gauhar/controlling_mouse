import pyautogui
import time

print("Current pos:", pyautogui.position())

pyautogui.moveTo(100, 100, duration=1)
print("Moved to top-left area:", pyautogui.position())
print("Current pos:", pyautogui.position())


time.sleep(1)

pyautogui.moveTo(1500, 800, duration=1)
print("Moved to bottom-right area:", pyautogui.position())
print("Current pos:", pyautogui.position())
