import os


def clear_screen():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)
