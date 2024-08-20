from titlepic import ManageTitlepics
from mainwindow import MainWindow
from launch import Launcher
from mainmodel import PortList, ProfileList
from port import Port
from PyQt5 import QtWidgets
from dbconnection import database, getPorts, getProfiles
from mainwindow import updateProfilePlaytime
import atexit
import argparse
import shutil

parser = argparse.ArgumentParser(prog="dlauncher", description="Launcher")
parser.add_argument('--profile_id', type=int)


@atexit.register
def DBSave():
    database.commit()
def default_port(row,name):
    return Port((
        row,
        name,
        shutil.which(name),
        None,
        "default:",
        ""
    ))

if __name__ == "__main__":
    args = parser.parse_args()
    if len(getPorts()) == 0:
        ports = PortList([default_port(0,"gzdoom"),default_port(1,"dsda-doom")])
    else:
        ports = PortList(getPorts())
    profiles = ProfileList(getProfiles())
    if args.profile_id:
        profile = profiles.findProfile(args.profile_id)
        launcher = Launcher(ports[profile.port], profile)
        playtime = launcher.LaunchPort()
        realplaytime = launcher.profile.playtime + playtime
        launcher.profile.playtime += playtime
        updateProfilePlaytime(launcher.profile, realplaytime)
    else:
        app = QtWidgets.QApplication([])
        titlepics = ManageTitlepics(profiles.profilelist)
        window = MainWindow(profiles, ports, titlepics)
        window.show()
        app.exec_()
    database.commit()
