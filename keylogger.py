from pynput.keyboard import Listener

valid_keys = ["Key.up", "Key.down", "Key.right", "Key.left", "Key.space","'c'"]

def on_press(key):
    with open("keylog.txt", "a") as f:
        k = str(key)
        if k in valid_keys:
            f.write(k + "\n")
 
with Listener(on_press=on_press) as listener:
    listener.join()
