from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import os


class ProfileList(QtCore.QAbstractListModel):
    """ QT-facing list of profiles

    """

    def __init__(self, profilelist=None):
        super(ProfileList, self).__init__()
        self.profilelist = profilelist or []

    def findProfile(self, ID):
        for profile in self.profilelist:
            if profile.rowid == ID:
                return profile

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.profilelist[index.row()])

    def rowCount(self, index):
        return len(self.profilelist)

    def findPort(self, port):
        for id, i in enumerate([i.name for i in self.profilelist]):
            if port in i:
                return id


class PortList(QtCore.QAbstractListModel):
    """ QT-facing list of ports
data function returns the displayed port

    """

    def __init__(self, portlist=None):
        super(PortList, self).__init__()
        self.portlist = portlist or []
        self.portdict = {}
        for port in portlist:
            self.portdict[port.name] = port

    def __getitem__(self, key):
        return self.portdict[key]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.portlist[index.row()])

    def rowCount(self, index):
        return len(self.portlist)

    def findPort(self, port):
        for id, i in enumerate([i.name for i in self.portlist]):
            if port in i:
                return id


class IWADList(QtCore.QAbstractListModel):
    """Documentation for IWADList

    """

    def __init__(self, iwads=None):
        super(IWADList, self).__init__()
        self.iwads = iwads or []

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return os.path.split(self.iwads[index.row()])[1]

    def findWAD(self, wad):
        for id, i in enumerate(self.iwads):
            if wad.lower() in i.lower():
                return id

    def mimeTypes(self):
        return ["application/zip", "application/x-doom-wad"]

    def rowCount(self, index):
        return len(self.iwads)


class CompatHandler(QtCore.QAbstractListModel):
    """Documentation for CompatHandler

    """

    def __init__(self, ports=None):
        super(CompatHandler, self).__init__()
        self.ports = ports
        self.compatlist = [port.compat for port in ports.portlist]
        self.updateData(0)

    def updateData(self, index):
        self.currport = index
        if len(self.compatlist) > 0:
            self.compat = self.compatlist[index]
            self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            print("----------")
            portlist = list(self.compatlist[self.currport].keys())
            print(portlist)
            # print(list(self.compatlist[self.currport].keys())[index.row()])
            return portlist[index.row()]

    def rowCount(self, index):
        try:
            return len(self.compatlist[self.currport])
        except IndexError:
            return 0
