#!/usr/bin/python

# Observe stdout from minecraft to determine log-in and achievements
# Call with bash LaunchServer.sh | python serverobserver.py

import sys
import re
import json
import time
import model_firebase as model
import config

file = "serverstatus.txt"
model.init_standalone(config)

def Observe():
    line = sys.stdin.readline()
    while(line):
        print(">" + line, end="")
        match = re.search(': (.+) joined the game', line)
        if match:
            this_player = model.Player(match.group(1), True)
            this_player.Set()

        match = re.search(': (.+) left the game', line)
        if match:
            this_player = model.Player(match.group(1), False)
            this_player.Set()

        match = re.search(': (.+) has just earned the achievement \[(.+)\]', line)
        if match:
            achievement = model.Achievement(match.group(1), match.group(2))
            model.Push(achievement)

        line = sys.stdin.readline()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h':
            print("Usage: " + sys.argv[0] + " [DUMPFILE_NAME]")
            exit()
        else:
            file = sys.argv[1]
    Observe()
