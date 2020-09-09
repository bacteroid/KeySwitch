# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:53:32 2020

@author: Mercteria

Version 1.0
"""

from pynput import keyboard
from pynput.keyboard import Key, Controller
#pip install pyenchant
import enchant

buffer = ""
prebuf = ""
keysnd = ['3','4','6','7']
switchlock = False
switchfail = 0
isauto = False
on = True

def on_press(inkey):
    try:
        global buffer
        buffer+=str(inkey.char)
    except:
        print('{0} pressed'.format(inkey))
        
def chkwrd(buffer):
    global prebuf
    d = enchant.Dict("en_US")
    print("==================")
    print("Chk:",buffer[:-1])
    if not d.check(buffer[:-1]) and not d.check(prebuf+buffer[:-1]):
        prebuf = ""
        print("Is Not Word !")
        print("==================")
        return False
    else:
        prebuf = ""
        print("Is Word !")
        print("==================")
        return True

def autoshift():
    global switchlock
    if switchlock:
        switchlock = False
    else:
        switchlock = True
    keyb = Controller()
    keyb.press(Key.shift)
    keyb.release(Key.shift)
    print("Auto Switch Language !")
    print("Now Switch is : ",str(switchlock))

def on_release(inkey):
    global buffer
    global prebuf
    global keysnd
    global switchlock
    global switchfail
    global isauto
    global on
    #print('{0} released'.format(inkey))
    try:
        if on:
            if inkey.char in keysnd or inkey == Key.space:
                chk = chkwrd(buffer)
                if not chk:
                    if not switchlock:
                        isauto = True
                        autoshift()
                    else:
                        print("Switched !")    
                else:
                    print("No Need to Switch !")
                buffer = ""
        else:
            print(buffer)
    except:
        if inkey == Key.esc:
            if on:
                on = False
                isauto = False
                switchlock = False
                buffer = ""
                print("Stop Lintening and reset !")
            else:
                on = True
                print("Start Lintening !")
            #return False
        elif inkey == Key.shift:
            if isauto:
                print("This is an auto press!")
                isauto = False
            else:
                autoshift()
                if len(buffer) > 0:
                    prebuf = buffer[-1]
                buffer = ""
                print("Switch : ",str(switchlock))
        elif inkey == Key.enter:
            buffer = ""
        elif inkey == Key.backspace:
            buffer = buffer[:-1]

# Collect events until released 
with keyboard.Listener(
     on_press=on_press, 
     on_release=on_release) as listener: 
    listener.join() 
    
