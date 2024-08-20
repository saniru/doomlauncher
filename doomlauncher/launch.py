import subprocess
import os
import sys
import shlex
import datetime
from discord import GameRPC, ClearRPC


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


class Launcher(object):
    """Handles launching of the game, and argument resolution"""

    def __init__(self, port, profile):
        self.port = port
        self.profile = profile
        self.args = self.ResolveArgs()

    def ResolveArgs(self):
        profilecomp = self.profile.compat
        profileargs = self.profile.fullargs
        portargs = self.port.GetPortArgs(profilecomp)
        if sys.platform == "win32":
            return (" ".join([portargs, profileargs]))
        else:
            return shlex.split(" ".join([portargs, profileargs]))

    def LaunchPort(self):
        start = datetime.datetime.now()
        with subprocess.Popen(self.args) as command:
            try:
                GameRPC(self.profile)
            except:
                pass
            command.poll()  # dummy
        end = datetime.datetime.now()
        try:
            ClearRPC()
        except:
            pass
        return (end-start).total_seconds()
