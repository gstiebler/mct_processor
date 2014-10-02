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

    def handle_starttag(self, tag, attrs):
        self.tagDepth = self.tagDepth + 1
        #self.fileDebug.write("Start tag: {0}, tag depth: {1}\n".format(tag, self.tagDepth))
        #self.fileDebug.write("     attr: |{0}|\n".format(attrs))
        
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
        self.fileDebug.write( "End tag  : {0}, tag depth: {1}\n".format(tag, self.tagDepth))
        
    def handle_data(self, data):
        if data == "\n":
            return
        self.fileDebug.write( "Valor  : {}\n".format(data))
        lastAttr = self.lastAttr
        lastAttr['value'] = data
        htmlItem = HTMLItem(copy.deepcopy(lastAttr))
        if not self.htmlItems.has_key(htmlItem.top):
            self.htmlItems[htmlItem.top] = {}
        self.htmlItems[htmlItem.top][htmlItem.left] = htmlItem
        self.fileDebug.write("lastAttr: {}\n".format(lastAttr))
        
        
def ehMCT(name):
    return name[:2] == "BF" or name[:2] == "OF" or name[:2] == "BS"

def isCircuitName(attr):
    if not attr.has_key('left') or not attr.has_key('id'):
        return False
    return attr['left'] == '40' and attr['id'] == 'f3'
        
        
fileDebug = open("debug.txt", "w")
file = open("output.txt", "w")

htmlStr = ""
for line in fileinput.input():
    htmlStr += line
   
    
parser = MyHTMLParser(file, fileDebug)
parser.feed(htmlStr)

sortedList = sorted(parser.htmlItems.items()) 

for sortedItem in sortedList:
    top = sortedItem[0]
    fileDebug.write("Top: {}\n".format(top))
    
    itemsInLine = sortedItem[1]
    sortedLine = sorted(itemsInLine.items())
    for lineItem in sortedLine:
        left = lineItem[0]
        htmlItem = lineItem[1]
        attrs = htmlItem.attrs
        if isCircuitName(attrs):
            fileDebug.write("Circuit name: {}\n".format(attrs['value']))
            circuit = {'name': attrs['value']}
        else:
            fileDebug.write("Left: {}, attrs: {}\n".format(left, attrs))
                
file.close()
fileDebug.close()