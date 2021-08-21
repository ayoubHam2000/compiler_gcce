import re
import sys

arg1 = sys.argv[1] #files
arg2 = sys.argv[2] #fullPath

files = {}
fullPath = arg2 + "/"

#region functions

#region getFiles

def setFiles(data):
    data = re.sub(r'[ ]+', '', data)
    data = data.split("\n")
    for item in data:
        a = item.split("->")
        if len(a) == 2:
            theFile = a[0]
            header = a[1]
            files[fullPath + theFile] = fullPath + header

def getFiles():
    params = sys.argv
    if len(params) >= 1:
        f = open(fullPath + arg1)
        setFiles(f.read())
        f.close()

#endregion

#region clear and define headers
def clearHeaders():
    already = []
    for item in files.keys():
        formatItem = fileName(files[item])
        name = formatItem.replace('.', '_').upper()
        if name not in already:
            out = open(files[item], "w")
            out.write(f'#ifndef {name}\n')
            out.write(f'#define {name}\n')
            out.write("\n\n")
            already.append(name)
            out.close()

def endHeaders():
    already = []
    for item in files.keys():
        name = files[item].replace('.', '_').upper()
        if name not in already:
            out = open(files[item], "a")
            out.write(f'#endif\n')
            already.append(name)
            out.close()

#endregion

#region prototypes

def formatData(data):
    data = re.sub(r'//.*?$', '', data)
    data = re.sub(r'/[\*].*?[\*]/', '', data)
    data = re.sub(r'\n+', '', data)
    data = re.sub(r' +', ' ', data)
    return data

def findMatches(data):
    #from setPrototypesFromSrcToDes (there is one space and no \n)
    typeRegex = "[A-z]+[ ]?[\\*]*"
    functionRegex = "[A-z_][A-z0-9_]*"
    argumentsRegex = "[A-z0-9_, \\*]*"
    theRegex = typeRegex + " " + functionRegex
    theRegex += "[ ]?\\([ ]?" + argumentsRegex + "[ ]?\\)[ ]?\\{"
    #theRegex += "\\{.*?\\}"
    return re.findall(theRegex, data)

def printComplete(src, des):
    sr = fileName(src)
    de = fileName(des)
    print(f'{sr} -> {de}')

def setPrototypesFromSrcToDes(src, des, onPrint = False):
    f = open(src, "r")
    out = open(des, "a")
    data = formatData(f.read())
    matches = findMatches(data)
    out.write(f'//++++++++++++++++++>> {fileName(src)}\n\n')
    for i in matches:
        item = re.sub('[\\{\\}]', '', i)
        item = re.sub('\\) ', ')', item)
        out.write(f'{item};\n')
        if onPrint:
            print(f'{item};\n')
    out.write("\n\n")
    f.close()
    out.close()
    printComplete(src, des)

def printContent(onPrint = False) :
    for item in files.keys() :
        setPrototypesFromSrcToDes(item, files[item], onPrint)

#endregion

#region command

def fileToCompile():
    c = ""
    for item in files.keys():
        i = fileName(item)
        c += f'{i} '
    return c

#endregion

#region utilities
def fileName(path):
    return re.sub(f'^{fullPath}', '', path)
#endregion

#endregion

getFiles()
clearHeaders()
printContent()
endHeaders()
print(fileToCompile())







