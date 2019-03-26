# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 19:07:59 2019

@author: mihir
"""

import pandas as pd

def inputCap(filename):
    lines = list(open(filename))
    capLabels = lines[0].strip().split()[1:]
    teamSlice = slice(1, len(lines), 2)
    capSlice = slice(2, len(lines), 2)
    teams = lines[teamSlice]
    caps = lines[capSlice]
    for i in range(len(caps)):
        caps[i] = caps[i].strip().split()
        for j in range(len(caps[i])):
                caps[i][j] = int(caps[i][j][1:].replace(",", ""))
                
    capData = pd.DataFrame(caps, columns=capLabels)
    return capData, capLabels, teams
    

filename = "./cap/2018.txt"
data, capLabels, teams = inputCap(filename)
