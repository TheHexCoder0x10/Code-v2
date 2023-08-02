import json


def getdata(FilePath):
    try:
        jsonfile = open(FilePath, 'r')
        json_content = json.load(jsonfile)
        jsonfile.close()
        return json_content
    except IOError: raise Exception('\nCould not open file.   :(\n')


def savedata(data, FilePath):
    jsonfile = open(FilePath, 'w')
    json.dump(data, jsonfile, indent=4)
    jsonfile.close()


def copydata(FilePath1, FilePath2):
    savedata(getdata(FilePath1), FilePath2)
