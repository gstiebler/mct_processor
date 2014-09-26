import fileinput
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):

    def __init__(self, outputFile, fileDebug):
        HTMLParser.__init__(self)
        self.outputFile = outputFile
        self.fileDebug = fileDebug
        self.tagDepth = 0
        self.lastAttr = ""
        self.insideBold = False

    def handle_starttag(self, tag, attrs):
        self.tagDepth = self.tagDepth + 1
        self.fileDebug.write("Start tag: {0}, tag depth: {1}\n".format(tag, self.tagDepth))
        if tag == "b":
            self.insideBold = True
        for attr in attrs:
            self.fileDebug.write("     attr: |{0}|\n".format(attr))
            self.lastAttr = attr
    def handle_endtag(self, tag):
        self.tagDepth = self.tagDepth - 1
        if tag == "b":
            self.insideBold = False
        self.fileDebug.write( "End tag  : {0}, tag depth: {1}\n".format(tag, self.tagDepth))
    def handle_data(self, data):
        self.fileDebug.write( "Valor  : %s\n" % (data))
        nameAttr = "stylefont-size:7.0pt;font-family:\"Times New Roman\",\"serif\""
        lastAttrStr = ''.join(self.lastAttr)
        if lastAttrStr == nameAttr:
            if self.insideBold:
                self.outputFile.write("Nome rota: {0}\n".format(data))
            else:
                self.outputFile.write("### Rota: {0}\n".format(data))
    def handle_comment(self, data):
        self.fileDebug.write( "Comment  : %s\n" % (data))
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        #self.fileDebug.write(" Named ent:{0}".format(c))
        
        
        
def ehLinhaRota(line):
    strings = line.split(" - ")
    if len(strings) > 1:
        for str in strings:
            if len(str.split(" ")) > 1:
                return False
                
            if len(str) < 3:
                return False
    else:
        return False
    return True
    
    
#def ehLinhaNome(line):
#    strings = line.split(" ")
#    if len(strings != 2:
#        return False
#    if len(strings[0]) < 3 or len(strings[1]) < 3:
#        return False
#    if not strings[0].isdigit():
#        return False
        
#    return True

fileDebug = open("debug.txt", "w")
file = open("output.txt", "w")

htmlStr = ""
for line in fileinput.input():
    htmlStr += line
    
parser = MyHTMLParser(file, fileDebug)
parser.feed(htmlStr)


file.close()
fileDebug.close()