import os
from genetic import *

levelNumber = input("Enter number of test case you want run : ")
populationNumber = int(input("Enter populationNumber : "))
mutationProb = input("Enter mutationProb : ")
crossover_split = int(input("Enter crossover_split : "))
specificSelection = int(input("Do you want to have specificSelection : (1/0)"))
crossoverType = int(input("Do you want to have crossoverType : (1/0)"))

f = open(os.path.join(os.path.dirname(__file__), "attachments/levels/level{}.txt".format(levelNumber)))
file = f.readline()
level = []
level.append(file)

g = Genetic(level=level,
            populationNumber=populationNumber, levelLen=len(level[0]), mutation=mutationProb,
            crossover_split=crossover_split, specificSelection=specificSelection, crossoverType=crossoverType)
g.initial_population()

g.do_algo()