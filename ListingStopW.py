
file_path='Stopwords.txt'

with open(file_path) as f:
    lines = f.readlines()

lines=[line.rstrip('\n') for line in lines]
lines.sort()    
print(lines)    


