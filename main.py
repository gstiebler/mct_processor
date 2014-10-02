import os
import html_to_csv

currPath = os.path.dirname(os.path.realpath(__file__))
HTMLDir = currPath + '\\saida_html' 

fileDebug = open("debug.txt", "w")
file = open("output.csv", "w")

count = 0
for currDir, dirs, files in os.walk(HTMLDir):

    for fileName in files:
        if fileName[:4] != "page" or fileName[-5:] != ".html":
            continue
            
        fileAndPath = "{}\\{}".format(currDir, fileName)
        inputFile = open(fileAndPath, "r")
        htmlStr = inputFile.read()
        inputFile.close()
        
            
        count = count + 1
        print "{} - Processando arquivo {}".format(count, fileAndPath)
        html_to_csv.convert(file, fileDebug, htmlStr)
        

file.close()
fileDebug.close()