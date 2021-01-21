import os
import webbrowser
import pyautogui
import time


def execute_task(task, data):
    if task == "Open File":
        _execute_file(data)
    elif task == "Open URL":
        _open_url(data)
    elif task == "Simulate Keyboard":
        _simulate_keyboard_input(data)
    elif task == "Write Text":
        _write_text(data)


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


def _write_text(text):
    pyautogui.write(text)

