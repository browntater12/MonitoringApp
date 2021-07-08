import os
import sys
import csv
import datetime
import pandas as pd
import numpy as np
import re
import argparse
import csv
#Creating Parser
parser = argparse.ArgumentParser(description='Program to parse exported CSV files from Blancco')
parser.add_argument('-f', '--file', type=str, help='A file.csv that you would like to parse')
args = parser.parse_args()
#print(args.file)


def __init__(self, fileName):
    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            column = ["^report", "^r_", "^blancco_data"]
            print("Not Found")
            for rowName in column:
                find = re.findall(rowName, line[0])
                if find:
                    print(find)
                
#Aggregates timestamps into one            
def elapseTime(line):
    try:
        list = line[4].split('/')
        sum = datetime.timedelta()
        for i in list:
            try:
                (h, m, s) = i.split(':')
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                sum += d
                line[4] = sum
            except ValueError:
                line[4] = '00:00:00'
    except AttributeError:
            line[4] = '00:00:00'


#Breaks the area down into more usable version
def area(line):
    try:
        match = re.search("-", line[16])
        if len(match) == 3:
            for i in range(4):
                (location, department, line, station) = i.split('-')
        elif len(match) == 2:
            for i in range(3):
                (location, department, station) = i.split('-')
        try:
            line[20] = location
            line[21] = department
            line[22] = line
            line[23] = station
        except NameError:
            pass
    except TypeError:
        pass
def erasureType(line):
    list = line[6].split('/')
    line[6] = list[0]


#Gives 1 or 0 based on state of erase
def erasureStatus(line):
    outcome = re.search("^Successful", line[2])
    if (outcome):
        line.append(1)
    else:
        line.append(0)


#Confirms that Smart Reset and IOS Apple Reset are working        
def smartCheck(line):
    smart = False
    ios = False 
    outcomes = line[2].split('/')
    kinds = line[5].split('/')
    for x in range(len(outcomes)): 
        if outcomes[x] == 'Successful':
            if kinds[x] == 'iOS smart reset (Verification)':
                smart = True
            elif kinds[x] == 'Apple iOS erasure' or kinds[x] == 'iOS smart reset (Apple iOS erasure)':
                ios = True 
    return smart, ios


#Aggregates the timestamps
def elapseTime(line):
    try:
        list = line[4].split('/')
        sum = datetime.timedelta()
        for i in list:
            try:
                (h, m, s) = i.split(':')
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                sum += d
                line[4] = sum
            except ValueError:
                line[4] = '00:00:00'
    except AttributeError:
        line[4] = '00:00:00'


#Confirms a successful erase for certain types of erases
def eraseType(line):
    smart = False
    ios = False
    outcomes = line[2].split('/')
    kinds = line[5].split('/')
    for x in range(len(outcomes)): 
        if outcomes[x] == 'Successful':
            if kinds[x] == 'iOS smart reset (Verification)':
                smart = True
            if kinds[x] == 'Apple iOS erasure' or kinds[x] == 'iOS smart reset (Apple iOS erasure)':
                ios = True
    line.append(smart)
    line.append(ios)


#Parses model names into friendlier model names
def modelNames(line):
    if line[7] == 'iPhone SE' or line[7] == 'iPhone SE 1st Gen':
        line[7] = 'iPhone SE (1st generation)'
    elif line[7] == 'iPhone SE 2nd Gen':
        line[7] = 'iPhone SE (2nd generation)'
    elif '6S' in line[7]:
        line[7] = line[7].replace('6S', '6s')
    elif '5S' in line[7]:
        line[7] = line[7].replace('5S', '5s')
    elif '5C' in line[7]:
        line[7] = line[7].replace('5C', '5c')
    if 'plus' in line[7]:
        line[7] = line[7].replace('plus', 'Plus')
    


# Parses bmc api return for easier transfer to data structure 
def parse(file): 
    with open(file, 'r', encoding="utf8") as inp, open("data/csv/parsedFile.csv", 'w', newline="", encoding="utf8") as out:
        reader = csv.reader(inp)
        writer = csv.writer(out)
        for line in reader:
            if line[0] == "Date":
                continue
            else:
                eraseType(line)
                modelNames(line)
                #erasureStatus(line)
                #elapseTime(line)
                writer.writerow(line)



