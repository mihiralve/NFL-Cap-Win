# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 19:07:59 2019

@author: mihir
"""

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def input_cap(filename):
    lines = list(open(filename))
    cap_labels = lines[0].strip().split()[1:]
    team_slice = slice(1, len(lines), 2)
    cap_slice = slice(2, len(lines), 2)
    teams = lines[team_slice]
    teams = [i.strip() for i in teams]
    caps = lines[cap_slice]
    for i in range(len(caps)):
        caps[i] = caps[i].strip().split()
        for j in range(len(caps[i])):
                caps[i][j] = int(caps[i][j][1:].replace(",", ""))
                
    capData = pd.DataFrame(caps, columns=cap_labels)
    capData['Team'] = teams
    return capData, cap_labels, teams
    
def input_records(filename):

    lines = list(open(filename))
    remove = {"\n", "x", "y", "z", "*"}
        
        
    lines_clean = []
    for i in range(len(lines)):
        if lines[i][0] not in remove:
            lines_clean.append(lines[i].strip().split())
            
    team_slice = slice(2, len(lines), 3)
    record_slice = slice(3, len(lines), 3)
    
    teams = lines_clean[team_slice]
    records = lines_clean[record_slice]
    
    record_str = re.sub("Arrow in down direction", "", lines[0])
    record_cols = record_str.strip().split("\t")[1:]
    
    numeric_cols = ["W", "L", "T"]
    recordData = pd.DataFrame(records, columns=record_cols)
    recordData[numeric_cols] = recordData[numeric_cols].apply(pd.to_numeric)
    
    labels = recordData['W'] + .5 * recordData['T']
    
    record_label = pd.DataFrame()
    record_label['Team'] = [i[0] for i in teams]
    record_label['Wins'] = labels
    
    return record_label

def get_data(year):
    cap_filename = "./cap/"+ year +".txt"
    nfc_filename = "./standings/" + year + "_nfc.txt"
    afc_filename = "./standings/" + year + "_afc.txt"
    
    data, cap_labels, teams = input_cap(cap_filename)
    
    nfc_records = input_records(nfc_filename)
    afc_records = input_records(afc_filename)
    records = pd.concat([nfc_records, afc_records])
    data = data.merge(records, on='Team')
    data.drop(['Team'], 1, inplace=True)
    
    return data

def get_qb_salary_vs_wins(data):
    plt.scatter(data['QB'], data['Wins'])
    plt.xlabel("QB Salary")
    plt.ylabel("Wins")
    
    trend = np.polyfit(data['QB'], data['Wins'], 1)
    trendpoly = np.poly1d(trend)
    
    plt.plot(data['QB'], trendpoly(data['QB']), label="y={:.2f}x+{:.2f}".format(trend[0], trend[1]))
    plt.legend() 
    
    plt.show()

if __name__ == "__main__":
    plt.figure()
    year = "2013"
    data_2013 = get_data(year)
    
    year = "2014"
    data_2014 = get_data(year)
    
    year = "2015"
    data_2015 = get_data(year)
    
    year = "2016"
    data_2016 = get_data(year)
    
    year = "2017"
    data_2017 = get_data(year)
    
    year = "2018"
    data_2018 = get_data(year)
    
    data_years = [data_2013, data_2014, data_2015, data_2016, data_2017, data_2018]
    data = pd.concat(data_years)
    get_qb_salary_vs_wins(data)



