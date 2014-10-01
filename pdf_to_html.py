import os

currPath = os.path.dirname(os.path.realpath(__file__))
PDFsDir = currPath + '\\PDFs'
HTMLDir = currPath + '\\saida_html' 
lenPDFsDir = len(PDFsDir)

for currDir, dirs, files in os.walk(PDFsDir):
    print "files {}".format(files)
        
    print "subdirs {}".format(currDir)
    
    baseDir = currDir[lenPDFsDir:]
    newHTMLDir = HTMLDir + baseDir
    if not os.path.exists(newHTMLDir):
        os.makedirs(newHTMLDir)