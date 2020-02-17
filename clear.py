
f = open("test.txt", "r")

data = f.read()

lines = data.split('\n')


for line in lines:
    print(line.split('Z   ')[1])