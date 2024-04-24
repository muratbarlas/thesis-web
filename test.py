from pynput.keyboard import Key, Listener

def on_press(key):
    if key.char == "x":
        print("left_press")
    if  key.char == "c":
        print('right_press')
    else:
        pass

def on_release(key):
    pass

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

