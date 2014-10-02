import fileinput
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import re
import copy

class HTMLItem(object):

    def __init__(self, attrs):
        self.attrs = attrs
        
        if attrs.has_key('left'):
            self.left = int(attrs['left'])
        else:
            self.left = 0
            
        if attrs.has_key('top'):
            self.top = int(attrs['top'])
        else:
            self.top = 0
 
    def __repr__(self):
        return "HTMLItem attrs: {}".format(self.attrs)

            
class MyHTMLParser(HTMLParser):

    def __init__(self, outputFile, fileDebug):
        HTMLParser.__init__(self)
        self.outputFile = outputFile
        self.fileDebug = fileDebug
        self.tagDepth = 0
        self.lastAttr = {}
        self.cableList = []
        self.htmlItems = {}
        self.lastTag = ""
        self.titleHeaderFontId = ""
        self.routeFontId = ""
        self.circuitNameFontId = ""
        
    def processFontsIds(self, styleStr):
        
        titleHeaderFont = "font-family:sans-serif; font-weight:bold; font-style:normal;"
        routeFont = "font-family:serif; font-weight:normal; font-style:normal;"
        circuitNameFont = "font-family:serif; font-weight:bold; font-style:normal;"

        fonts = styleStr.split("\n")
        
        fontsIds = {}
        print len(fonts)
        for font in fonts:
            if font is None:
                continue
                
            regexResult = re.search('\#(f\d)', font)
            if regexResult is None:
                continue
                
            fontId = regexResult.group(1)
            fontDescription = re.search('\{\s(.*)\s\}', font).group(1)
            
            fontsIds[fontDescription] = fontId
            
            
        #self.fileDebug.write("{}\n".format(fontsIds))
        
        if not fontsIds.has_key(titleHeaderFont) or not fontsIds.has_key(routeFont) or not fontsIds.has_key(circuitNameFont):
            return
        
        self.titleHeaderFontId = fontsIds[titleHeaderFont]
        self.routeFontId = fontsIds[routeFont]
        self.circuitNameFontId = fontsIds[circuitNameFont]
        
        self.fileDebug.write("titleHeaderFontId {}\n".format(self.titleHeaderFontId))
        self.fileDebug.write("routeFontId {}\n".format(self.routeFontId))
        self.fileDebug.write("circuitNameFontId {}\n".format(self.circuitNameFontId))
        
        
    def handle_starttag(self, tag, attrs):
        self.tagDepth = self.tagDepth + 1
        #self.fileDebug.write("Start tag: {0}, tag depth: {1}\n".format(tag, self.tagDepth))
        #self.fileDebug.write("     attr: |{0}|\n".format(attrs))
        
        self.lastTag = tag
        if tag == "div":
            for attr in attrs:
                if attr[0] == "style":
                    left = re.search('.*left\:(\d*)px.*', attr[1]).group(1)
                    top = re.search('.*top\:(\d*)px.*', attr[1]).group(1)
                    self.lastAttr['left'] = left
                    self.lastAttr['top'] = top
        elif tag == "span":
            for attr in attrs:
                if attr[0] == "style":
                    font_size = re.search('.*font-size\:(\d*)px.*', attr[1]).group(1)
                    self.lastAttr['font_size'] = font_size
                elif attr[0] == "id":
                    self.lastAttr['id'] = attr[1]
                    
    def handle_endtag(self, tag):
        self.tagDepth = self.tagDepth - 1
        #self.fileDebug.write( "End tag  : {0}, tag depth: {1}\n".format(tag, self.tagDepth))
        
    def handle_data(self, data):
        if data == "\n":
            return
            
        if self.lastTag == "style":
            #self.fileDebug.write( "style tag: {}\n".format(data))
            self.processFontsIds(data)
            return
            
        lastAttr = self.lastAttr
        lastAttr['value'] = data
        htmlItem = HTMLItem(copy.deepcopy(lastAttr))
        if not self.htmlItems.has_key(htmlItem.top):
            self.htmlItems[htmlItem.top] = {}
        self.htmlItems[htmlItem.top][htmlItem.left] = htmlItem
        #self.fileDebug.write("lastAttr: {}\n".format(lastAttr))
        
        
def isMCT(name):
    return name[:2] == "BF" or name[:2] == "BS"

def hasCircuitName(itemsInLine, htmlParser):
    if not itemsInLine.has_key(40):
        return False
        
    if not itemsInLine[40].attrs.has_key('id'):
        return False
    
    return itemsInLine[40].attrs['id'] == htmlParser.circuitNameFontId
        

def hasRoute(itemsInLine, htmlParser):
    if not itemsInLine.has_key(40):
        return False
        
    return itemsInLine[40].attrs['id'] == htmlParser.routeFontId
    
    
def getAttr(itemsInLine, X, fileDebug):
    if itemsInLine.has_key(X):
        return itemsInLine[X].attrs['value']
    
    DELTA_MAX = 15
    for key, value in itemsInLine.items():
        if abs(key - X) < DELTA_MAX:
            return value.attrs['value']
    
    sortedList = sorted(itemsInLine.items()) 
    
    previous = ""
    next = ""
    for i in range(len(sortedList)):
        key = sortedList[i][0]
        value = sortedList[i][1]
        if key > X:
            next = value.attrs['value']
            if i > 0:
                previous = sortedList[i - 1][1].attrs['value']
            break
    
    fileDebug.write("X not found: {}. Avaliable: {}\n".format(X, itemsInLine))
    return "{} | {}".format(previous, next)
    
def outputCircuit(circuit, MCT, fileAndPath, file):
    
    file.write("{};".format(circuit['name']))
    file.write("{};".format(MCT))
    outputOrder = ['secc', 'type', 'route', 'espec']
    for outputName in outputOrder:
        str = ""
        if circuit.has_key(outputName):
            str = circuit[outputName]
        file.write("{};".format(str))
    file.write("{};".format(fileAndPath))
    
    file.write("\n")
    
        

def convert(file, fileDebug, htmlStr, fileAndPath, circuit):
        
    parser = MyHTMLParser(file, fileDebug)
    parser.feed(htmlStr)

    sortedList = sorted(parser.htmlItems.items()) 

    state = "none"
    nameX = 40
    typeX = 504
    especX = 656
    seccX = 606
    routeX = 40
    
    for sortedItem in sortedList:
        top = sortedItem[0]
        itemsInLine = sortedItem[1]
        fileDebug.write("Top: {}\n".format(top))
        fileDebug.write("state: {}\n".format(state))
        fileDebug.write("itemsInLine: {}\n".format(itemsInLine))
        
        sortedLine = sorted(itemsInLine.items())
        for lineItem in sortedLine:
            left = lineItem[0]
            htmlItem = lineItem[1]
            attrs = htmlItem.attrs
            #fileDebug.write("Left: {}, attrs: {}\n".format(left, attrs))
            
        if state == "none" or state == "route":
            if hasCircuitName(itemsInLine, parser):
                
                fileDebug.write("hasCircuitName\n")
                circuit = {
                        'name': getAttr(itemsInLine, nameX, fileDebug),
                        'type': getAttr(itemsInLine, typeX, fileDebug),
                        'espec': getAttr(itemsInLine, especX, fileDebug),
                    }
                state = "circuit_header"
            elif hasRoute(itemsInLine, parser):
                fileDebug.write("hasRoute\n")
                route = getAttr(itemsInLine, routeX, fileDebug)
                route = route.split(' - ')
                
                for item in route:
                    if isMCT(item):
                        outputCircuit(circuit, item, fileAndPath, file)
            else:
                state = "none"
        elif state == "circuit_header":
            circuit['secc'] = getAttr(itemsInLine, seccX, fileDebug)
            state = "route"
            
    return circuit
     