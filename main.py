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
        self.htmlItems = []

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
        self.fileDebug.write( "Valor  : {}\n".format(data))
        lastAttr = self.lastAttr
        lastAttr['value'] = data
        self.fileDebug.write("lastAttr: {}\n".format(lastAttr))
        self.htmlItems.append(HTMLItem(copy.deepcopy(lastAttr)))
        
        
    
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


sortedHTMLItems = sorted(parser.htmlItems)

for htmlItem in sortedHTMLItems:
    fileDebug.write("{}\n".format(htmlItem.attrs))
                
file.close()
fileDebug.close()