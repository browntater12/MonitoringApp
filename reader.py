import csv 
import re
import shelve 
import parsed


#Determines if model has had a successful smart wipe
def smartReset(line):
    outcomes = line[2].split('/')
    kinds = line[5].split('/')
    for x in range(len(outcomes)): 
        if outcomes[x] == 'Successful':
            if kinds[x] == 'iOS smart reset (Verification)':
                return True


#Determines if model has had a successful firmware wipe
def iosReset(line):
    outcomes = line[2].split('/')
    kinds = line[5].split('/')
    for x in range(len(outcomes)): 
        if outcomes[x] == 'Successful':
            if kinds[x] == 'Apple iOS erasure' or kinds[x] == 'iOS smart reset (Apple iOS erasure)':
                return True


#Determines fmip status
def fmipCheck(status):
    if status == "Locked": return "locked"
    elif status == "Unlocked": return "unlocked"
    else: return 'unknown'


#Determines if we have a successful wipe record
def eraseCheck(status):
    outcome = re.search("^Successful", status)
    if (outcome):
        return "success"
    else:
        return "fail"


#Determines manufacturer TODO(Not Apple = Android)
def manufacturer(status):
    if status == "Apple, Inc.":
        return "apple"
    else: 
        return "android"


#Creates a new model in the version 
def modelData(line,x):
    if not (x):
        iPhone = {
            "model": line[7],
            "smartReset" : False,
            "iosReset" : False, 
            "fmip" : {"unlocked": 0, "locked": 0, "unknown": 0},
            "success" : 0,
            "fail" : 0,
            "apple": 0,
            "android": 0
        }

    if (smartReset(line)):
        iPhone["smartReset"] = True
    if (iosReset(line)):
        iPhone["iosReset"] = True
    iPhone["fmip"][fmipCheck(line[12])] += 1
    iPhone[eraseCheck(line[2])] += 1
    iPhone[manufacturer(line[6])] += 1
    return iPhone


#Determines if model is in version or not
def newModel(line):
    for x in range(len(history[line[14]])):
        if history[line[14]][x]['model'] != line[7]:
            continue
        else: 
            return (False, x)
    return (True, x) 


#Changes existing model data
def addData(model):
    if (smartReset(line)):
        model["smartReset"] = True
    if (iosReset(line)):
        model["iosReset"] = True
    model["fmip"][fmipCheck(line[12])] += 1
    model[eraseCheck(line[2])] += 1
    model[manufacturer(line[6])] += 1
    
#MAIN
parsed.parse('data\csv\pull.csv')

file = open("data\csv\parsedFile.csv", "r", encoding="utf8")
reader = csv.reader(file)

data = shelve.open('history.db')
try:
    history = data['history']
    exist = True
except KeyError: 
    history = {'versions': []}
    exist = False

# Read csv lines and push data to data structure  
for line in reader:
#Add version to historical versions
    if line[14] not in history['versions']:
        history["versions"] += [line[14]]
#Add a new version & model to data structure
    if line[14] not in history: 
        history[line[14]] = [modelData(line,0)]
    else:
#Add new model to version
        if(newModel(line)[0]):
            history[line[14]].append(modelData(line,0))
        else:
#Add data to existing model
            addData(history[line[14]][newModel(line)[1]])
        
       
#TODO
# "averageIos" : "{holder}", 
# "averageAndroid" : "{holder}"

data['history'] = history

file.close()
data.close()    