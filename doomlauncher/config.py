from launch import get_script_path
import json
with open(get_script_path() + "/config.json") as configfile:
    config = json.load(configfile)
