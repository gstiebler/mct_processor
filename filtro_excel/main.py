from xlrd import open_workbook
import xlwt
import os

currPath = os.path.dirname(os.path.realpath(__file__))
saidaDir = currPath + '\\saida\\' 
        
def returnList(inputDict, key):
    if inputDict.has_key(key):
        return inputDict[key]
    else:
        return []
        
def returnDict(inputDict, key):
    if inputDict.has_key(key):
        return inputDict[key]
    else:
        return {}
    


outputFile = open('out.txt', 'w')

wb = open_workbook('OK MCT.xlsx')
inputSheet = wb.sheets()[0]

MCTs = {}
for row in range(inputSheet.nrows):
    values = []
    
    MCT = inputSheet.cell(row, 2).value
    area = MCT[2:6]
    
    for col in range(inputSheet.ncols):
        value = inputSheet.cell(row, col).value
        values.append(value)
           
    MCTsInArea = returnDict(MCTs, area)
    circuitsInMCT = returnList(MCTsInArea, MCT)
    circuitsInMCT.append( values )
    MCTsInArea[MCT] = circuitsInMCT
    MCTs[area] = MCTsInArea

    

for item in MCTs.items():
    area = item[0]
    MCTsFromArea = item[1]
    print "Area: {}".format( area )
    
    outputFile.write(" +++++++++ area: {}\n".format(area) )
    os.makedirs("{}\\{}".format(saidaDir, area))
    for MCTItems in MCTsFromArea.items():
        MCT = MCTItems[0]
        circuits = MCTItems[1]
        outputFile.write(" +++++++++ MCT: {}\n".format(MCT) )
        outputDir = "{}\\{}\\{}".format(saidaDir, area, MCT)
        os.makedirs(outputDir)
        
        workbookOutput = xlwt.Workbook() 
        sheet = workbookOutput.add_sheet(MCT) 
        
        for i in range(len(circuits)):
            outputFile.write("circuito: {}\n".format(circuits[i][2]) )
            for j in range(len(circuits[i])):
                sheet.write(i, j, circuits[i][j]) # row, column, value  
            
        outputFileStr = "{}\\{}.xls".format(outputDir, MCT)
        workbookOutput.save(outputFileStr) 

    
outputFile.close()