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
            self.lastAttr = ''.join(attr)
            self.fileDebug.write("     attr: |{0}|\n".format(self.lastAttr))
    def handle_endtag(self, tag):
        self.tagDepth = self.tagDepth - 1
        if tag == "b":
            self.insideBold = False
        self.fileDebug.write( "End tag  : {0}, tag depth: {1}\n".format(tag, self.tagDepth))
    def handle_data(self, data):
        self.fileDebug.write( "Valor  : %s\n" % (data))
        nameAttr = "stylefont-size:7.0pt;font-family:\"Times New Roman\",\"serif\""
        cableTypeAttr = "stylefont-size:7.0pt;font-family:\"Times New Roman\",\"serif\";\nletter-spacing:-.35pt"
        concepAttr = "stylefont-size:7.0pt;font-family:\"Times New Roman\",\"serif\";\nletter-spacing:-.15pt"
        lastAttrStr = self.lastAttr
        if lastAttrStr == nameAttr:
            if self.insideBold:
                #self.outputFile.write("Nome rota: {0}\n".format(data))
                self.cableList.append({'cableName': data, 'route': ''})
            else:
                #self.outputFile.write("### Rota: {0}\n".format(data))
                if len(self.cableList) > 0:
                    self.cableList[-1]['route'] += data
                
        if lastAttrStr == cableTypeAttr:
            #self.outputFile.write(" +++++++++++++ Cable type: {}".format(data))
            
            if len(self.cableList) > 0:
                if self.cableList[-1].has_key('type'):
                    if len(data) >= 3:
                        self.cableList[-1]['type'] = self.cableList[-1]['type'] + " | " + data
                else:
                    self.cableList[-1]['type'] = data
                
        if lastAttrStr == concepAttr:
            self.outputFile.write(" +++++++++++++ Cable concep: {}\n".format(data))
            if len(self.cableList) > 0:
                self.cableList[-1]['concep'] = data
            
    def handle_comment(self, data):
        self.fileDebug.write( "Comment  : %s\n" % (data))
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        #self.fileDebug.write(" Named ent:{0}".format(c))
        
        
    
def ehMCT(name):
    if name[:2] == "BF" or name[:2] == "OF" or name[:2] == "BS":
        return True
    else:
        return False

        
        
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
    cableType = ""
    concep = ""
    if item.has_key('type'):
        cableType = item['type']
    if item.has_key('concep'):
        cableType = item['concep']
    route = route.replace('\n', ' ')
    route = route.split(' - ')
    #file.write("Cable: {0}, route: {1}\n".format(cableName, route))
    for itemInRoute in route:
        if ehMCT(itemInRoute):
            #file.write("MCT: {0}\n".format(itemInRoute))
            currObj = {'name': cableName, 'type': cableType, 'concep': concep}
            if MCTs.has_key(itemInRoute):
                MCTs[itemInRoute].append(currObj)
            else:
                MCTs[itemInRoute] = [currObj]

for mctName in MCTs:
    file.write("MCT name: {0}\n".format(mctName))
    for circuit in MCTs[mctName]:
        circuitStr = circuit['name'].replace(" ", "")
        type = circuit['type'].replace("\n", "")
        concep = circuit['concep']
        file.write("Circuit: {0}, type: {1}, concep: {2}\n".format(circuitStr, type, concep))
                
file.close()
fileDebug.close()