from pypresence import Presence
import time
# got some things from examples in pypresence
try:
    client_id = ""
    RPC = Presence(client_id)
    RPC.connect()
except:
    pass

def GameRPC (profile):
    RPC.update(state=f"Playing {profile.name} ({profile.port})")

def ClearRPC ():
    RPC.clear()
