import os
import html_to_csv

currPath = os.path.dirname(os.path.realpath(__file__))
HTMLDir = currPath + '\\saida_html' 

fileDebug = open("debug.txt", "w")
file = open("output.csv", "w")

count = 0

lastCircuit = ""
for currDir, dirs, files in os.walk(HTMLDir):

    fileCounter = 1
    while True:
        fileAndPath = "{}\\page{}.html".format(currDir, fileCounter)
        fileCounter = fileCounter + 1
            
        if not os.path.isfile(fileAndPath):
            fileDebug.write("Arquivo nao existe: {}\n".format(fileAndPath))
            break
            
        inputFile = open(fileAndPath, "r")
        htmlStr = inputFile.read()
        inputFile.close()
        
        count = count + 1
        msg = "{} - Processando arquivo {}\n".format(count, fileAndPath)
        print msg
        fileDebug.write(msg)
        lastCircuit = html_to_csv.convert(file, fileDebug, htmlStr, fileAndPath, lastCircuit)

file.close()
fileDebug.close()