import fileinput

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
    
    
def ehLinhaNome(line):
    strings = line.split(" ")
    if len(strings) != 2:
        return False
    if len(strings[0]) < 3 or len(strings[1]) < 3:
        return False
    if not strings[0].isdigit():
        return False
        
    return True


file = open("output.txt", "w")

for line in fileinput.input():
    if ehLinhaRota(line):
        file.write("### LINHA ROTA ### ")
    if ehLinhaNome(line):
        file.write("+++ LINHA NOME +++ ")
    file.write(line)


file.close()