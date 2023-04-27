__author__    = "Ferris Linde"
__copyright__ = "Copyright (C) 2023 Ferris Linde"
__license__   = "Public Domain"
__version__   = "3.0"
__github__    = "https://github.com/ferris/cordr"

'''
Cordr, a macOS ChatGPT-in-the-background tool.
In order for the key-logging functions to work, this script must be granted root or accessibility access.
'''

from pynput import keyboard
import re
import urllib.parse
import urllib.request
import html
import os
import openai


def passIn(phrase):
    global newPhrase
    # newPhrase = translate(phrase, lanTo, lanFrom)
    newPhrase = chatgpt(phrase)
    # print("Translated: " + phrase + " ; to: " + newPhrase)
    print("Response: " + newPhrase)
    # notify("{} to {}".format(lanFrom, lanTo), newPhrase)
    os.system('afplay /System/Library/Sounds/Bottle.aiff')

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

# PYNPUT

def on_release(key):
    global going
    global starter
    global userInput
    global kb
    global newPhrase
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
                passIn(userInput)
                print(newPhrase)
                userInput = ""
        elif going:
            userInput += key.char
    except Exception as e:
        print(e)
        print('special key {0} pressed'.format(key))
        if going:
            # special modifiers for user input
            if key == keyboard.Key.space:
                userInput += " "
            elif key == keyboard.Key.backspace:
                userInput = userInput[:-1]
        elif key == keyboard.Key.caps_lock:
            typeOut(newPhrase)

def typeOut(s):
    # TODO: try to somehow add punctuation
    s = s.lower()
    for char in s:
        if ord(char) >= 97 and ord(char) <= 122:
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


# GOOGLE TRANSLATE

agent = {'User-Agent':
             "Mozilla/4.0 (\
             compatible;\
             MSIE 6.0;\
             Windows NT 5.1;\
             SV1;\
             .NET CLR 1.1.4322;\
             .NET CLR 2.0.50727;\
             .NET CLR 3.0.04506.30\
             )"}


def chatgpt(msg):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": msg},
        ]
    )
    return resp.choices[0].message.content


def translate(to_translate, to_language="auto", from_language="auto"):
    # language is shortcut (es is spanish, fr is french, en is english)
    base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    to_translate = urllib.parse.quote_plus(to_translate)
    link = base_link % (to_language, from_language, to_translate)
    request = urllib.request.Request(link, headers=agent)
    raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = html.unescape(re_result[0])
    return (result)


if __name__ == '__main__':
    global going
    global starter
    global userInput
    global kb
    global newPhrase
    going = False
    starter = ""
    userInput = ""
    newPhrase = ""
    # Collect events until released
    kb = keyboard.Controller()
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
