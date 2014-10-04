from xlrd import open_workbook
import xlwt

workbookOutput = xlwt.Workbook() 
sheet = workbookOutput.add_sheet("Aba1") 

outputFile = open('out.txt', 'w')

wb = open_workbook('OK MCT.xlsx')
inputSheet = wb.sheets()[0]

print 'Sheet:', inputSheet.name
for row in range(inputSheet.nrows):
    values = []
    for col in range(inputSheet.ncols):
        value = inputSheet.cell(row, col).value
        #sheet.write(row, col, value) # row, column, value   
        
        if type(value) is unicode:
            value = value.encode('ascii','replace')
        else:
            value = str(value)
                
        outputFile.write(value)
    outputFile.write("\n")
print

    
workbookOutput.save("foobar.xls") 
outputFile.close()