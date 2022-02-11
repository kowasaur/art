# TODO: Start with big brush

# Make a shortcut to open the foreground colour picker with ?
# Select brush tool
# Set brush size to 10
# Set smoothing to 0%
# Open blank 1000 x 1000 document

from random import randint
from typing import Literal
from pynput.mouse import Listener
from pynput.keyboard import Controller, Key
import pyautogui

TIME = 0.3 # time it takes to move cursor

# number of pixels moved by arrow keys
# also the width of the brush
width = 10
keyboard = Controller()
max_x = max_y = min_x = min_y = None

def increase_width():
    global width
    if width < 10:
        width += 1
    elif width < 50:
        width += 5
    elif width < 100:
        width += 10
    elif width < 200:
        width += 25
    else:
        raise Exception("increase_width not sufficient")

def rand_colour():
    keyboard.type("?")
    colour = "%06x" % randint(0, 0xFFFFFF)
    keyboard.type(colour)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def move_random():
    x = randint(min_x, max_x)
    y = randint(min_y, max_y)
    pyautogui.moveTo(x, y, duration = TIME)

def drag(x: Literal[-1, 0, 1], y: Literal[-1, 0, 1]):
    pyautogui.dragRel(x * width * 2, y * width * 2, duration = TIME)
    pos = pyautogui.position()
    if pos.y > max_y:
        pyautogui.moveTo(pos.x, max_y)
    elif pos.y < min_y:
        pyautogui.moveTo(pos.x, min_y)
    pos = pyautogui.position()
    if pos.x > max_x:
        pyautogui.moveTo(max_x, pos.y)
    elif pos.x < min_x:
        pyautogui.moveTo(min_x, pos.y)

def on_click(x, y, _, pressed):
    global max_x, max_y, min_x, min_y
    if not pressed: return
    
    if min_x == None:
        min_x = x
        min_y = y
    elif max_x == None:
        max_x = x
        max_y = y
        return False

print("Alt tab to photoshop and then click the top left corner and bottom right corner of the canvas")
    
with Listener(on_click=on_click) as listener:
    listener.join()

print(f"{max_x=}\n{max_y=}\n{min_x=}\n{min_y=}")

with open("keylog.txt", "r") as f:
    keys = f.readlines()

move_random()
rand_colour()

for key in keys:
    match key.strip():
        case "Key.left":
            drag(-1, 0)
        case "Key.right":
            drag(1, 0)
        case "Key.up":
            drag(0, 1)
        case "Key.down":
            drag(0, -1)
        case "Key.space":
            rand_colour()
            move_random()
        case "'c'":
            keyboard.type("]")
            increase_width()
            move_random()
        case _:
            raise Exception("Unknown key: " + key.strip())
