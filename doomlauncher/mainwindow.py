from launch import get_script_path, Launcher
from shortcut_linux import profile_shortcut
from PyQt5 import QtWidgets, uic
from profilewindow import ProfileWindow
from PyQt5.QtGui import QPixmap
from profile import DescribeProfile
from dbconnection import portc


class PortWindow(QtWidgets.QMainWindow):
    def __init__(self, ports, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, profilelist, portlist, titlepics, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        super(MainWindow, self).__init__()
        uic.loadUi(get_script_path()+'/main.ui', self)
        self.setupVars(profilelist, portlist, titlepics)
        self.profiledialog.backpointer = self
        self.profilelist.setModel(self.profiles)
        self.profilelist.selectionModel().selectionChanged.connect(self.updateProfile)
        self.setWindowTitle("DOOM LAUNCHER")

    def setupVars(self, profilelist, portlist, titlepics):
        self.ports = portlist
        self.titlepics = titlepics
        self.profiledialog = ProfileWindow(self.ports)
        self.profiles = profilelist
        self.profiledialog.profilelist = self.profilelist
        self.profiledialog.profiles = self.profiles

    def createProfile(self):
        self.profiledialog.updating = False
        self.profiledialog.show()
        self.profiles.layoutChanged.emit()

    def editProfile(self):
        self.profiledialog.updating = True
        profile = self.profiledialog
        self.profiledialog.plistindex = self.profilelist.selectedIndexes()[
            0].row()
        self.profiledialog.loadProfile(self.getCurrentProfile())
        profile.show()
        self.profiles.layoutChanged.emit()

    def updateProfile(self, item):
        try:
            currprof = self.getCurrentProfile()
            self.titlepic.setPixmap(QPixmap.fromImage(
                self.titlepics[currprof.rowid]))
            self.profileinfo.setText(DescribeProfile(currprof))
        except (AttributeError,IndexError):
            self.profileinfo.setText("")
        self.profiles.layoutChanged.emit()

    def deleteProfile(self, item):
        index = self.profilelist.selectedIndexes()[0]
        if index:
            removee = self.profiles.profilelist[index.row()]
            portc.execute("DELETE FROM Profiles WHERE ID = ?;",
                          (removee.rowid,))
            del self.profiles.profilelist[index.row()]
            self.profiles.layoutChanged.emit()
            self.profilelist.clearSelection()

    def getCurrentProfile(self):
        try:
            index = self.profilelist.selectedIndexes()[0]
            currprof = self.profiles.profilelist[index.row()]
            return currprof
        except IndexError:
            return None

    def startGame(self, lc):
        currprof = self.getCurrentProfile()
        currport = self.ports[currprof.port]
        launcher = Launcher(currport, currprof)
        self.setWindowTitle(f"Playing {currprof.name} ({currprof.port})")
        playtime = launcher.LaunchPort()
        self.setWindowTitle("DOOM LAUNCHER")
        realplaytime = launcher.profile.playtime + playtime
        launcher.profile.playtime += playtime
        updateProfilePlaytime(launcher.profile, realplaytime)

    def makeShortcut(self):
        profile_shortcut(self.getCurrentProfile())

    def editPorts(self):
        pass


def updateProfilePlaytime(profile, playtime):
    db_id = profile.rowid
    print(db_id)
    portc.execute(
        "UPDATE Profiles SET playtime = ?  WHERE rowid = ?;", (playtime, db_id))
