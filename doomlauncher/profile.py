from os import path
from datetime import timedelta
from math import floor


def DescribeProfile(profile):
    string = ""
    string += f"\n{profile.name}\n{10*'-'}\n"
    string += f"IWAD={path.split(profile.iwad)[1]}\nPWADS=\n{10*' '}- "
    string += f"\n{10*' '}- ".join([path.split(i)[1] for i in profile.pwads])
    string += f"\n{10*'-'}\n\nFor {profile.port}"
    string += f"\n\"{profile.compat}\" Compatibility mode\n"
    string += f"\nplayed for: {str(timedelta(seconds=floor(profile.playtime)))}"
    return string


class Profile(object):
    """Represents a profile to be launched"""

    def __init__(self, data):
        schema = ["rowid", "name", "iwad", "pwads", "port",
                  "compat", "config", "playtime", "image"]
        for count, ele in enumerate(data):
            setattr(self, schema[count], ele)

        self.pwads = self.pwads.splitlines()
        # if not hasattr(self, 'image'):
        #     self.image = GetProfileTitlepic(self)
        if self.config is None or not isinstance(self.config,str):
            self.config = ""
        self.wadstring = " ".join([f"-file \"{wad}\""
                                   for wad in self.pwads])
        self.fullargs = f"-iwad {self.iwad} " + self.wadstring \
            + " " + self.config

    def __repr__(self):
        return "<Profile({self.name}, {self.iwad})>"

    def __str__(self):
        return (f"{self.name}: {path.split(self.iwad.upper())[1]}"
                f" with {len(self.pwads)} PWADS")
