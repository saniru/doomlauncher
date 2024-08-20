import sqlite3
import tempfile
from port import Port
from profile import Profile

database = sqlite3.connect(tempfile.gettempdir() + "/testdbdlauncher.db")
database.cursor().execute("CREATE TABLE IF NOT EXISTS Ports(name, path, icon, compat, config)")
database.cursor().execute("CREATE TABLE IF NOT EXISTS Profiles(name, iwad, pwads, port,compat, config, playtime, image)")
portc = database.cursor()
profc = database.cursor()


def getPorts():
    return [Port(i) for i in database.execute("SELECT rowid,* FROM Ports")]


def getProfiles():
    return [Profile(i) for i in database.execute("SELECT rowid,* FROM Profiles")]
