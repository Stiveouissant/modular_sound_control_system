import os
import webbrowser
import pyautogui
import time
from datetime import datetime


def execute_task(task, data):
    if task == "Open File":
        _execute_file(data)
    elif task == "Open URL":
        _open_url(data)
    elif task == "Simulate Keyboard":
        _simulate_keyboard_input(data)
    elif task == "Simulate Mouse":
        _simulate_mouse_input(data)
    elif task == "Write Text":
        _write_text(data)
    elif task == 'Take Screenshot':
        _take_screenshot()


def _execute_file(filepath):
    os.startfile(filepath)


def _open_url(url):
    webbrowser.open(url, 2, True)


def _simulate_keyboard_input(script):
    script_list = script.split(";")
    del script_list[-1]
    print(script_list)
    for sc in script_list:
        inst = sc.split(",")
        if inst[0] == 'comma':
            inst[0] = ','
        elif inst[0] == 'semicolon':
            inst[0] = ';'
        print(inst)
        if inst[1] == "Down":
            pyautogui.keyDown(inst[0])
        elif inst[1] == "Press":
            pyautogui.press(inst[0])
        else:
            pyautogui.keyUp(inst[0])
        time.sleep(float(inst[2]))


def _simulate_mouse_input(script):
    script_list = script.split(";")
    del script_list[-1]
    print(script_list)
    for sc in script_list:
        inst = sc.split(",")
        print(inst)
        if inst[0] == 'Relative':
            pyautogui.move(int(inst[1]), int(inst[2]), float(inst[3]))
        else:
            pyautogui.moveTo(int(inst[1]), int(inst[2]), float(inst[3]))

        if inst[4] == 'scroll-up':
            pyautogui.scroll(int(inst[6]))
        elif inst[4] == 'scroll-down':
            pyautogui.scroll(-int(inst[6]))
        else:
            if inst[5] == 'Press':
                pyautogui.click(button=inst[4], clicks=int(inst[6]), interval=float(inst[7]))
            elif inst[5] == 'Down':
                pyautogui.mouseDown(button=inst[4])
            else:
                pyautogui.mouseUp(button=inst[4])
            time.sleep(float(inst[8]))


def _write_text(text):
    pyautogui.write(text)


def _take_screenshot():
    datename = str(datetime.now())
    datename = datename.replace(":", "")
    pyautogui.screenshot('screenshots/'+datename+'.png')

