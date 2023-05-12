import utils

fp, fn = utils.filePaths()
for p, n in zip(fp, fn): 
    text = utils.readFile(p, n)

    print(text)