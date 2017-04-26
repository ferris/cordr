
#  You _must_ turn on assistive devices under Accessibility prefpane
# for any of this code to work. Otherwise it won't do anything.
from Cocoa import *
from Foundation import *
from PyObjCTools import AppHelper
import keycode
import string
import sys
import subprocess
import re
import urllib2
import urllib
import HTMLParser
import os


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, handler)


def handler(event):
    global going
    global starter
    global userInput
    if event.type() == NSKeyDown and keycode.tostring(event.keyCode()) in string.printable:
        if keycode.tostring(event.keyCode()) == "`" or keycode.tostring(event.keyCode()) == "\\":
            #print("Goin:" + str(going))
            if not going:
                print("going = true")
                going = True
                os.system('afplay /System/Library/Sounds/Frog.aiff')
                starter = keycode.tostring(event.keyCode())
            else:
                going = False
                #print("going = false")
                if starter == "`":
                    passIn(userInput, "es", "en")
                else:
                    passIn(userInput, "en", "es")
                userInput = ""

        elif going:
            userInput += keycode.tostring(event.keyCode())
            #print("aadd user in")
            #print(str(going))

        #print keycode.tostring(event.keyCode())


def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()

# ----------


# Back End
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


def unescape(text):
    parser = HTMLParser.HTMLParser()
    return (parser.unescape(text))


def translate(to_translate, to_language="auto", from_language="auto"):
    # language is shortcut (es is spanish, fr is french, en is english)
    base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    to_translate = urllib.quote_plus(to_translate)
    link = base_link % (to_language, from_language, to_translate)
    request = urllib2.Request(link, headers=agent)
    raw_data = urllib2.urlopen(request).read()

    data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def passIn(phrase, lanTo, lanFrom):
    newPhrase = translate(phrase, lanTo, lanFrom)
    print("Translated: " + phrase + " ; to: " + newPhrase)
    write_to_clipboard(newPhrase)
    os.system('afplay /System/Library/Sounds/Bottle.aiff')

#--------
if __name__ == '__main__':
    global going
    global starter
    global userInput
    going = False
    starter = "`"
    userInput = ""
    main()