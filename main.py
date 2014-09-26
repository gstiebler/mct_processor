import fileinput
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):

    def __init__(self, outputFile):
        HTMLParser.__init__(self)
        self.outputFile = outputFile
        self.tagDepth = 0

    def handle_starttag(self, tag, attrs):
        self.tagDepth = self.tagDepth + 1
        self.outputFile.write("Start tag: {0}, tag depth: {1}".format(tag, self.tagDepth))
        for attr in attrs:
            self.outputFile.write("     attr: {0}".format(attr))
    def handle_endtag(self, tag):
        self.tagDepth = self.tagDepth - 1
        self.outputFile.write( "End tag  : {0}, tag depth: {1}".format(tag, self.tagDepth))
    def handle_data(self, data):
        self.outputFile.write( "Data  : %s" % (data))
    def handle_comment(self, data):
        self.outputFile.write( "Comment  : %s" % (data))
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        #self.outputFile.write(" Named ent:{0}".format(c))
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        self.outputFile.write( "Decl  : %s" % (data))
        
        
        
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


file = open("output.txt", "w")

htmlStr = ""
for line in fileinput.input():
    htmlStr += line
    
parser = MyHTMLParser(file)
parser.feed(htmlStr)


file.close()