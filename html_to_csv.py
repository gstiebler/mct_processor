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
        
    def __cmp__(self, other):
        if self.top < other.top:
            return -1
        elif self.top > other.top:
            return 1
        else:
            return self.left < other.left

            
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
        
        #self.fileDebug.write("{} {} {}\n".format(self.titleHeaderFontId, self.routeFontId, self.circuitNameFontId))
        
        

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
    
    
def getAttr(itemsInLine, fileDebug):
    
    sortedList = sorted(itemsInLine.items()) 
    
    result = []
    for item in sortedList:
        result.append(item[1].attrs['value'])
    
    return result
    
def outputCircuit(circuit, MCT, file):
    header_1 = circuit['header_1']
    header_2 = circuit['header_2']

    file.write("{};".format(MCT))
    for item in header_1:
        file.write("{};".format(item))
    for item in header_2:
        file.write("{};".format(item))
    
    file.write("\n")

def convert(file, fileDebug, htmlStr):
        
    parser = MyHTMLParser(file, fileDebug)
    parser.feed(htmlStr)

    sortedList = sorted(parser.htmlItems.items()) 

    state = "none"
    nameX = 40
    #typeX = 504
    #especX = 656
    #seccX = 606
    routeX = 40

    for sortedItem in sortedList:
        top = sortedItem[0]
        itemsInLine = sortedItem[1]
        #fileDebug.write("Top: {}\n".format(top))
        
        #fileDebug.write("state: {}\n".format(state))
        sortedLine = sorted(itemsInLine.items())
        for lineItem in sortedLine:
            left = lineItem[0]
            htmlItem = lineItem[1]
            attrs = htmlItem.attrs
            #fileDebug.write("Left: {}, attrs: {}\n".format(left, attrs))
            
        if state == "none" or state == "route":
            if hasCircuitName(itemsInLine, parser):
                circuit = {
                        'header_1': getAttr(itemsInLine, fileDebug)
                    }
                state = "circuit_header"
            if state == "route":
                if hasRoute(itemsInLine, parser):
                    route = getAttr(itemsInLine, fileDebug)
                    route = route[0].split(' - ')
                    
                    for item in route:
                        if isMCT(item):
                            outputCircuit(circuit, item, file)
                else:
                    state = "none"
        elif state == "circuit_header":
            circuit['header_2'] = getAttr(itemsInLine, fileDebug)
            state = "route"
            
     