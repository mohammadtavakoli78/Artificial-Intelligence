import os

levelNumber = input("Enter number of test case you want run : ")    # get input number of puzzle from user

f = open(os.path.join(os.path.dirname(__file__)+"/", "puzzles/puzzle{}.txt".format(levelNumber)))   # open file

base = []
f.readline()    # read dimension of file
for line in f:  # read file and base
    base.append(line.split())
