import os

for file in os.listdir("./"):
    os.rename(file, file.replace('.2000M','.200M'))
