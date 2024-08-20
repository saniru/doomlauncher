import os
import winshell

from launch import get_script_path
from win32com.client import Dispatch
# https://www.blog.pythonlibrary.org/2010/01/23/using-python-to-create-shortcuts/
dir_path = os.path.dirname(os.path.realpath(__file__))


def profile_shortcut(profile):
    desktop = winshell.desktop()
    path = os.path.join(desktop, f"{profile.name}.lnk")
    target = 'C:\\Windows\\System32\\cmd.exe'
    args = f'/k "pipenv run {get_script_path()}\\main.py --profile_id {profile.rowid}'
    wDir = get_script_path()
    # https://pbpython.com/windows-shortcut.html
    with winshell.shortcut(path) as shortcut:
        shortcut.path = target
        shortcut.arguments = args
        shortcut.description = f"{profile.name} - {profile.port}"
        shortcut.working_directory = wDir
