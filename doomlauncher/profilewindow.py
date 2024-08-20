from PyQt5 import QtWidgets, uic
from launch import get_script_path
from titlepic import ManageTitlepics
from mainmodel import IWADList, CompatHandler
from profile import Profile
from dbconnection import portc
from config import config


class ProfileWindow(QtWidgets.QMainWindow):
    """ Window with profile data

    """

    def __init__(self, ports, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        super(ProfileWindow, self).__init__()
        uic.loadUi(get_script_path()+'/profile.ui', self)

        self.setAcceptDrops(True)
        self.profile_wadlist.setAcceptDrops(True)
        self.profile_wadlist.setDragEnabled(True)
        self.profile_port.currentIndexChanged.connect(lambda:
                                                      self.compats.updateData(
                                                          self.profile_port.currentIndex()))
        self.setupVars(config, ports)
        self.setupModels()
        # self.profile_wadlist.viewport().installEventFilter(self)
        validmimes = ["application/zip", "application/x-doom-wad"]
        self.profile_wadlist.mimeTypes = lambda: validmimes
        self.setWindowTitle("Profile Editor")

    def loadProfile(self, profile):
        self.currplaytime = profile.playtime
        self.profileid = profile.rowid
        self.pwads.iwads = profile.pwads
        self.pwads.layoutChanged.emit()
        self.profile_iwad.setCurrentIndex(self.iwads.findWAD(profile.iwad))
        self.profile_name.setText(profile.name)
        print(self.ports[profile.port])
        self.profile_port.setCurrentIndex(self.ports.findPort(profile.port))
        self.profile_config.setPlainText(profile.config)

    def setupVars(self, config, ports):
        self.updating = False
        self.iwads = IWADList(config['iwads'])
        self.pwads = IWADList()
        self.ports = ports
        self.compats = CompatHandler(self.ports)

    def setupModels(self):
        self.profile_port.setModel(self.ports)
        self.profile_compat.setModel(self.compats)
        self.profile_iwad.setModel(self.iwads)
        self.profile_wadlist.setModel(self.pwads)

    def removeWAD(self, arg):
        index = self.profile_wadlist.selectedIndexes()[0]
        if index:
            del self.pwads.iwads[index.row()]
            self.pwads.layoutChanged.emit()
            self.profile_wadlist.clearSelection()

    def addWAD(self, arg, wads=None):
        if wads is None:
            chooser = QtWidgets.QFileDialog()
            chooser.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            chooser.exec_()
            wads = chooser.selectedFiles()
        for wad in wads:
            self.pwads.iwads.append(wad)
        self.pwads.layoutChanged.emit()

    def saveProfile(self, arg):
        name = self.profile_name.text()
        iwad = self.iwads.iwads[self.profile_iwad.currentIndex()]
        wad_list = "\n".join(self.pwads.iwads)
        port = self.ports.portlist[self.profile_port.currentIndex()].name
        compat = self.profile_compat.currentText()
        config = self.profile_config.toPlainText()

        if self.updating:
            portc.execute("UPDATE Profiles SET Name = ?, IWAD = ?, PWADS = ?"
                          ", Port = ?, Compatibility = ?,Config = ?"
                          ",Playtime = ?  WHERE ID = ?;",
                          (name,
                           iwad,
                           wad_list,
                           port,
                           compat,
                           config,
                           self.currplaytime,
                           self.profileid))
            new_profile = Profile(
                (portc.lastrowid, name, iwad, wad_list,
                 port, compat, config, self.currplaytime))
            self.profiles.profilelist[self.plistindex] = new_profile
            self.backpointer.titlepics = ManageTitlepics(
                self.profiles.profilelist, portc.lastrowid)
        else:
            portc.execute("INSERT INTO Profiles (name, iwad, pwads, port,compat, config, playtime,image)"
                          " VALUES (?,?,?,?,?,?,?,?)",
                          (name, iwad, wad_list, port, compat, config, 0.0, None))
            new_profile = Profile((portc.lastrowid, name, iwad,
                                   wad_list, port, compat, config, 0.0))
            self.profiles.profilelist.append(new_profile)
            self.backpointer.titlepics = ManageTitlepics(
                self.profiles.profilelist, portc.lastrowid)
        self.backpointer.updateProfile(new_profile)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mimetypes = event.mimeData()
        if (event.mimeData().hasUrls()):
            urllist = mimetypes.urls()
            pathlist = [i.toLocalFile() for i in urllist]
            self.addWAD(True, pathlist)
