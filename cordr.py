__author__ = "Ferris Linde"
__copyright__ = "Copyright (C) 2023 Ferris Linde"
__license__ = "Public Domain"
__version__ = "3.0"
__github__ = "https://github.com/ferris/cordr"

import os
import openai
from pynput import keyboard


def pass_in(phrase):
    global gpt_resp
    gpt_resp = chatgpt(phrase)
    print("ChatGPT Response: " + gpt_resp)
    notify("ChatGPT Response", gpt_resp)
    os.system('afplay /System/Library/Sounds/Bottle.aiff')


def notify(title, text):
    os.system("osascript -e 'display notification \"{}\" with title \"{}\"".format(text, title))


def on_release(key):
    global going
    global starter
    global userInput
    global kb
    global gpt_resp
    try:
        print('{0} released'.format(key.char))
        if key.char == '\\':
            print("activator pressed!")
            if not going:
                print("going = true")
                going = True
                os.system('afplay /System/Library/Sounds/Frog.aiff')
                starter = key.char
            else:
                print("going = false")
                going = False
                pass_in(userInput)
                print(gpt_resp)
                userInput = ""
        elif going:
            userInput += key.char
    except Exception as e:  # TODO: refine/rethink this except statement
        print(e)
        print('special key {0} pressed'.format(key))
        if going:
            # special modifiers for user input
            if key == keyboard.Key.space:
                userInput += " "
            elif key == keyboard.Key.backspace:
                userInput = userInput[:-1]
        elif key == keyboard.Key.caps_lock:
            type_out(gpt_resp)


def type_out(s):
    # TODO: try to somehow add punctuation
    s = s.lower()
    for char in s:
        if 97 <= ord(char) <= 122:
            # lower case a-z
            kb.press(char)
            kb.release(char)
        elif ord(char) == 32:
            # space
            kb.press(keyboard.Key.space)
            kb.release(keyboard.Key.space)
        elif ord(char) == 225:
            # á
            with kb.pressed(keyboard.Key.alt):
                kb.press('e')
                kb.release('e')
            kb.press('a')
            kb.release('a')
        elif ord(char) == 233:
            # é
            with kb.pressed(keyboard.Key.alt):
                kb.press('e')
                kb.release('e')
            kb.press('e')
            kb.release('e')
        elif ord(char) == 237:
            # í
            with kb.pressed(keyboard.Key.alt):
                kb.press('e')
                kb.release('e')
            kb.press('i')
            kb.release('i')
        elif ord(char) == 243:
            # ó
            with kb.pressed(keyboard.Key.alt):
                kb.press('e')
                kb.release('e')
            kb.press('o')
            kb.release('o')
        elif ord(char) == 250:
            # ú
            with kb.pressed(keyboard.Key.alt):
                kb.press('e')
                kb.release('e')
            kb.press('u')
            kb.release('u')
        elif ord(char) == 241:
            # ñ
            with kb.pressed(keyboard.Key.alt):
                kb.press('n')
                kb.release('n')
            kb.press('n')
            kb.release('n')
        else:
            print('could not type {}'.format(char))


def chatgpt(msg):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": msg},
        ]
    )
    return resp.choices[0].message.content


if __name__ == '__main__':
    global going
    global starter
    global userInput
    global kb
    global gpt_resp
    going = False
    starter = ""
    userInput = ""
    gpt_resp = ""
    # Collect events until released
    kb = keyboard.Controller()
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
