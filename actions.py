
import pyautogui
import time

pyautogui.FAILSAFE = False

last_click_time = 0
last_double_click_time = 0

def move_mouse(x, y):
    pyautogui.moveTo(x, y, duration=0)

def left_click():
    pyautogui.click()

def right_click():
    pyautogui.click(button="right")

def double_click():
    pyautogui.doubleClick()

def mouse_down():
    pyautogui.mouseDown()

def mouse_up():
    pyautogui.mouseUp()

def scroll(amount):
    pyautogui.scroll(amount)

def alt_tab():
    pyautogui.hotkey("alt", "tab")

def next_tab():
    pyautogui.hotkey("ctrl", "tab")

def prev_tab():
    pyautogui.hotkey("ctrl", "shift", "tab")

def minimize():
    pyautogui.hotkey("win", "down")

def maximize():
    pyautogui.hotkey("win", "up")
