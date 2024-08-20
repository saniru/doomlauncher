import omg
import os
import tempfile
from launch import get_script_path
from PIL import Image
from PIL.ImageQt import ImageQt
from os.path import abspath


def ManageTitlepics(profilelist, force=-1):
    cachedir = tempfile.gettempdir() + "/titlepic_cache"
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)
    cachefiles = os.listdir(cachedir)
    cachefiles.sort(key=int)
    currpics = [os.path.join(cachedir, pic) for pic in cachefiles]
    titlepics = {}
    for i in currpics:
        titlepics[int(os.path.basename(i))] = ImageQt(
            Image.open(i))
    # if the profile's rowid doesnt have an image create it, or if we are
    # forcing with force
    for profile in profilelist:
        i = (int(profile.rowid))
        if (i == force) or (str(i) not in cachefiles):
            titlepics[i] = GetProfileTitlepic(profile)
            titlepics[i].save(cachedir + str(i), "PNG")
    return titlepics


def GetWadTitlepic(wad):
    try:
        modfile = omg.WAD(abspath(wad))
        try:
            return omg.Graphic(modfile.graphics['TITLEPIC'])
        except KeyError:
            # moonbld has TITLEPIC in PP_
            return omg.Graphic(modfile.patches['TITLEPIC'])
    except Exception:
        pass


def GetProfileTitlepic(profile):
    for mod in profile.pwads:
        try:
            titlelump = GetWadTitlepic(mod)
            if titlelump is not None:
                break
        except KeyError:
            print("NO TITLEPIC")
        except OSError:
            print("NOT A WAD, MAYBE PK3")
    try:
        titlepic = titlelump.to_Image()
    except Exception:
        try:
            titlepic = GetWadTitlepic(profile.iwad).to_Image('RGBA')
        except Exception:
            titlepic = Image.open("fallback.png")

    return ImageQt(titlepic)
