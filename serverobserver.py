#!/usr/bin/python

# Observe stdout from minecraft to determine log-in and achievements
# Call with bash LaunchServer.sh | python serverobserver.py

import sys
import re
import json
import time

file = "serverstatus.txt"

class Player:
    def __init__(self, name, online=True):
        self.name = name
        self.online = online
        self.last_seen = time.time()

    def Login(self):
        self.last_seen = time.time()
        self.online = True

    def Logout(self):
        self.last_seen = time.time()
        self.online = False

    def ToObject(self):
        return {"name":self.name, "online":self.online, "last_seen":time.time()}

class PlayerList:
    def __init__(self):
        self.list={}

    def Login(self, player):
        if not player in self.list:
            self.list[player] = Player(player)
        else:
            self.list[player].Login()

    def Logout(self, player):
        if not player in self.list:
            self.list[player] = Player(player, False)
        else:
            self.list[player].Logout()

    def StopServer(self, player):
        for key in self.list:
            self.list[key].Logout()

    def ToObject(self):
        object = {}
        for key in self.list:
            object[key] = self.list[key].ToObject()
        return object

def Dump(playerlist):
    f = open("serverstatus.txt", 'w')
    json.dump(playerlist.ToObject(), f)
    f.close()

def Observe():
    list = PlayerList()
    
    while(True):
        line = sys.stdin.readline()
        match = re.search(': (.+) joined the game', line)
        if match:
            list.Login(match.group(1))
            Dump(list)

        match = re.search(': (.+) left the game', line)
        if match:
            list.Logout(match.group(1))
            Dump(list)

if __name__ == "__main__":
    global file
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h':
            print "Usage: " + sys.argv[0] + " [DUMPFILE_NAME]"
            exit()
        else:
            file = sys.argv[1]
    Observe()
