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
#    data.drop(['Team'], 1, inplace=True)
    
    return data

def get_qb_salary_vs_wins(data):
    plt.figure()
    plt.scatter(data['QB'], data['Wins'])
    plt.xlabel("QB Salary")
    plt.ylabel("Wins")
    
    trend = np.polyfit(data['QB'], data['Wins'], 1)
    trendpoly = np.poly1d(trend)
    
    plt.plot(data['QB'], trendpoly(data['QB']), label="y={:.2f}x+{:.2f}".format(trend[0], trend[1]))
    plt.legend() 
    
    plt.show()
    
def remove_rookie_contracts(year, data, remove=True):
    rookies_2013 = ["Bills", "Jets", "Redskins", "Jaguars", 
                    "Raiders", "Eagles", "Panthers", "Colts", 
                    "Titans", "Vikings", "Texans", "Rams", "49ers",
                    "Bengals", "Browns", "Dolphins"]
    rookies_2014 = ["Vikings", "Jaguars", "Titans", "Raiders"
                    "Bills", "Jets", "Redskins", "Buccaneers"
                    "Eagles", "Panthers", "Colts", "Dolphins"]
    rookies_2015 = ["Buccaneers", "Titans", "Vikings", "Jaguars", 
                    "Raiders", "Bills", "Broncos", "Redskins"]
    rookies_2016 = ["Rams", "Buccaneers", "Browns", "Titans", 
                    "Cowboys", "Eagles", "Jaguars", "Broncos",
                    "Raiders"]
    rookies_2017 = ["Browns", "Texans", "Bears", "Buccaneers", "Rams",
                    "49ers", "Packers", "Titans", "Cowboys", "Eagles",
                    "Colts", "Jaguars", "Jets", "Broncos"]
    rookies_2018 = ["Ravens", "Cardinals", "Jets", "Bills", "49ers",
                    "Browns", "Texans", "Chiefs", "Buccaneers", 
                    "Bears", "Rams", "Jaguars", "Bengals", "Titans",
                    "Cowboys", "Eagles"]
    
    rookies = {"2013": rookies_2013, "2014": rookies_2014, "2015": rookies_2015,
               "2016": rookies_2016, "2017": rookies_2017, "2018": rookies_2018}
    teams = []
    
    if remove:
        for ind, row in data.iterrows():
            if row['Team'] not in rookies[year]:
                teams.append(row)
    else:
        for ind, row in data.iterrows():
            if row['Team'] in rookies[year]:
                teams.append(row)
        
    
    df = pd.DataFrame()
    df = df.append(teams)
    
    return df

def get_offense_only(data):
    plt.figure()
    plt.scatter(data['Offense'], data['Wins'])
    plt.xlabel("Offensive Spending")
    plt.ylabel("Wins")
    
    trend = np.polyfit(data['Offense'], data['Wins'], 1)
    trendpoly = np.poly1d(trend)
    
    plt.plot(data['Offense'], trendpoly(data['Offense']), label="y={:.2f}x+{:.2f}".format(trend[0], trend[1]))
    plt.legend() 
    
    plt.show()
    
def get_defense_only(data):
    plt.figure()
    plt.scatter(data['Defense'], data['Wins'])
    plt.xlabel("Defensive Spending")
    plt.ylabel("Wins")
    
    trend = np.polyfit(data['Defense'], data['Wins'], 1)
    trendpoly = np.poly1d(trend)
    
    plt.plot(data['Defense'], trendpoly(data['Defense']), label="y={:.2f}x+{:.2f}".format(trend[0], trend[1]))
    plt.legend() 
    
    plt.show()

if __name__ == "__main__":
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
#    get_qb_salary_vs_wins(data)
    
    data_2013_2 = remove_rookie_contracts("2013", data_2013)
    data_2014_2 = remove_rookie_contracts("2014", data_2014)
    data_2015_2 = remove_rookie_contracts("2015", data_2015)
    data_2016_2 = remove_rookie_contracts("2016", data_2016)
    data_2017_2 = remove_rookie_contracts("2017", data_2017)
    data_2018_2 = remove_rookie_contracts("2018", data_2018)
    
    data_years_2 = [data_2013_2, data_2014_2, data_2015_2, data_2016_2, data_2017_2, data_2018_2]
    data_2 = pd.concat(data_years_2)
#    get_qb_salary_vs_wins(data_2)
    
    get_offense_only(data)
    get_defense_only(data)
    



