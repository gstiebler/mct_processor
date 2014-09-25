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


file = open("output.txt", "w")

for line in fileinput.input():
    if ehLinhaRota(line):
        file.write("### LINHA ROTA ### ")
    file.write(line)


file.close()