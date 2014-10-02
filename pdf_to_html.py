import os

currPath = os.path.dirname(os.path.realpath(__file__))
PDFsDir = currPath + '\\PDFs'
HTMLDir = currPath + '\\saida_html' 
lenPDFsDir = len(PDFsDir)
pdf2htmlExe = "pdftohtml.exe"

count = 0
for currDir, dirs, files in os.walk(PDFsDir):
    baseDir = currDir[lenPDFsDir:]
    newHTMLDir = HTMLDir + baseDir
    if not os.path.exists(newHTMLDir):
        os.makedirs(newHTMLDir)
        
    for file in files:
        if file[-4:].upper() != ".PDF":
            continue
			
        fileAndPath = "{}\\{}".format(currDir, file)
        outputDir = "{}\\{}".format(newHTMLDir, file[:-4])
        command = "{} \"{}\" \"{}\"".format(pdf2htmlExe, fileAndPath, outputDir)
        count = count + 1
        print "{} - Convertendo arquivo {}...".format(count, fileAndPath)
        print command
        os.system(command)