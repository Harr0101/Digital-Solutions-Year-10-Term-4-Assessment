import os



fileName = input("File name: ")+".txt"
f = open(fileName)

lines = f.readlines()
f.close()

columns = (input("Which columns: ")).split()

finalName = input("Final file name: ")+ ".txt"
if os.path.exists(finalName):
  os.remove(finalName)
f = open(finalName,"a")

for line in lines:
    line = line.split()
    for column in columns:
        f.write(line[int(column)-1]+"\n")

f.close()