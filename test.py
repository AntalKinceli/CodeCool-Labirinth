from pynput import keyboard
import curses
mainscreen = curses.initscr()
curses.noecho()  # limits input for curses only
curses.cbreak()  # unbufered input mode
# keypad mode so special buttons will be returned easely
mainscreen.keypad(1)
curses.start_color()  # initialize the default color set
curses.curs_set(0)  # hides cursor

keypress = ""
keyrelease = ""


def yea():
    print("yea")


def on_press(key, asd=0):
    global keypress
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        keypress += str(key) + ", "
        yea()
        return False
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    global keyrelease
    print('{0} released'.format(
        key))

    return False


with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()

print(keypress)

with keyboard.Listener(
        on_release=on_release) as listener:
    listener.join()

print(keyrelease)
