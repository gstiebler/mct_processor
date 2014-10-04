from xlrd import open_workbook
import xlwt

def createOrAppend(inputDict, key, value):
    if inputDict.has_key(key):
        inputDict[key].append(value)
    else:
        inputDict[key] = [value]
        
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
    

workbookOutput = xlwt.Workbook() 
sheet = workbookOutput.add_sheet("Aba1") 

outputFile = open('out.txt', 'w')

wb = open_workbook('OK MCT.xlsx')
inputSheet = wb.sheets()[0]

print 'Sheet:', inputSheet.name

MCTs = {}
for row in range(inputSheet.nrows):
    values = []
    
    MCT = inputSheet.cell(row, 2).value
    area = MCT[2:6]
    
    for col in range(inputSheet.ncols):
        value = inputSheet.cell(row, col).value
        values.append(value)
           
    #createOrAppend(MCTs, area, values)
    MCTsInArea = returnDict(MCTs, area)
    circuitsInMCT = returnList(MCTsInArea, MCT)
    circuitsInMCT.append( values )
    MCTsInArea[MCT] = circuitsInMCT
    MCTs[area] = MCTsInArea

    

for item in MCTs.items():
    area = item[0]
    MCTsFromArea = item[1]
    
    outputFile.write(" +++++++++ area: {}\n".format(area) )
    
    for MCTItems in MCTsFromArea.items():
        MCT = MCTItems[0]
        circuits = MCTItems[1]
        outputFile.write(" +++++++++ MCT: {}\n".format(MCT) )
        
        for circuit in circuits:
            outputFile.write("circuito: {}\n".format(circuit[2]) )


    #sheet.write(row, col, value) # row, column, value   

    
workbookOutput.save("foobar.xls") 
outputFile.close()