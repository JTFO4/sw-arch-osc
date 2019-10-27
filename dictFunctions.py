import json
from initializeDB import *
#
#
#we will store dictionaries as json strings in the database
# 
#Rows are returned as lists of dictionaries for easy manipulation
#
#easy to and from json functions to speed things along
#

#sql = "SELECT item FROM inventoryTable"

def returnRowDicts(sql, param=None):
    if(param == None):
        result = c.execute(sql)
    else:
        result = c.execute(sql, (param,))
    result = c.fetchall()
    items = []
    for row in result:
        items.append(dict(row))
    return items

def toJSON(Dump):
    jsonDump = json.dumps(Dump)
    return jsonDump

def fromJSON(Load):
    jsonLoad = json.loads(Load)
    return jsonLoad


#results = c.execute(sql)
#results = c.fetchall()
#itemDict = returnRowDicts(sql)
#print(itemDict)



