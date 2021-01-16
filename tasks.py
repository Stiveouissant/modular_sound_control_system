import os


def execute_task(task, data):
    if task == "Open File":
        _execute_file(data)


def _execute_file(filepath):
    os.startfile(filepath)
