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
        self.cableList = []

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
                self.cableList.append({'cableName': data, 'route': ''})
            else:
                self.outputFile.write("### Rota: {0}\n".format(data))
                self.cableList[-1]['route'] += data
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
    
def ehMCT(name):
    if name[:2] == "BF" or name[:2] == "OF" or name[:2] == "BS":
        return True
    else:
        return False
    
    
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

MCTs = {}
for item in parser.cableList:
    route = item['route']
    cableName = item['cableName']
    route = route.replace('\n', ' ')
    route = route.split(' - ')
    file.write("Cable: {0}, route: {1}\n".format(cableName, route))
    for itemInRoute in route:
        if ehMCT(itemInRoute):
            file.write("MCT: {0}\n".format(itemInRoute))
            if MCTs.has_key(itemInRoute):
                MCTs[itemInRoute].append(cableName)
            else:
                MCTs[itemInRoute] = [cableName]

for mctName in MCTs:
    file.write("MCT name: {0}\n".format(mctName))
    for circuit in MCTs[mctName]:
        file.write("Circuit: {}\n".format(circuit))
                
file.close()
fileDebug.close()