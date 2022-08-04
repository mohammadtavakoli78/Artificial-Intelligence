from game import *
import random
from copy import *
from matplotlib import pyplot as plt
from gui import *


class Genetic:
    def __init__(self, level, populationNumber, levelLen, mutation, crossover_split, specificSelection, crossoverType):
        self.level = level
        self.point = 0
        self.initialPopulation = []
        self.populationNumber = populationNumber
        self.levelLen = levelLen
        self.mutationProb = mutation
        self.populationFitness = {}
        self.step = 0
        self.crossover_split = crossover_split
        self.specificSelection = specificSelection
        self.crossoverType = crossoverType
        self.minFitness = []
        self.maxFitness = []
        self.avgFitness = []

    def initial_population(self):
        for i in range(0, self.populationNumber):
            population = ''.join(random.choices(['0', '1', '2'], k=self.levelLen))
            while population in self.initialPopulation:
                population = ''.join(random.choices(['0', '1', '2'], k=self.levelLen))
            self.initialPopulation.append(population)
            self.populationFitness[population] = self.fitness_function(population)

    def fitness_function(self, action):
        fitness = 0
        return_tuple = self.run_algo(action)
        if return_tuple[0]:
            fitness += self.levelLen//2
        fitness += return_tuple[1]
        return fitness

    def selection(self):
        if not self.specificSelection:
            a = {k: v for k, v in sorted(self.populationFitness.items(), key=lambda item: item[1], reverse=True)}

            d1 = dict(list(a.items())[:len(a) // 2])

            return d1
        else:
            sum = 0
            probList = []
            for key, value in self.populationFitness.items():
                sum += value
                probList.append(value)
            probList = [x / sum for x in probList]

            d = {}

            a = random.choices(list(self.populationFitness.keys()), weights=probList, k = len(self.populationFitness) //2)
            for i in a:
                d[i] = self.fitness_function(i)

            while len(d) < len(self.populationFitness)//2:
                a = random.choices(list(self.populationFitness.keys()), weights=probList, k=1)
                d[a[0]] = self.fitness_function(a[0])
            return d

    def crossover(self, popultaion):
        temp = deepcopy(popultaion)
        popLen = len(temp)

        for i in range(popLen // 2 + 1):

            newStr1 = list(temp.items())[0][0]
            newStr2 = list(temp.items())[1][0]

            while newStr1 in temp or newStr2 in temp:
                a = random.randint(0, popLen - 1)
                b = random.randint(0, popLen - 1)

                popultaionList = list(popultaion.keys())
                d1 = random.choice(popultaionList)
                d2 = random.choice(popultaionList)

                if self.crossoverType:
                    str1 = d1[0:self.crossover_split]
                    str2 = d1[self.crossover_split:self.crossover_split*2]
                    str3 = d1[self.crossover_split*2:]
                    str4 = d2[0:self.crossover_split]
                    str5 = d2[self.crossover_split:self.crossover_split*2]
                    str6 = d2[self.crossover_split*2:]

                    newStr1 = list(str1 + str5 + str3)
                    newStr2 = list(str4 + str2 + str6)
                else:
                    str1 = d1[0:self.crossover_split]
                    str2 = d1[self.crossover_split:]
                    str3 = d2[0:self.crossover_split]
                    str4 = d2[self.crossover_split:]

                    newStr1 = list(str1 + str4)
                    newStr2 = list(str3 + str2)
                newStr1 = ''.join(newStr1)
                newStr2 = ''.join(newStr2)

            temp[newStr1] = self.fitness_function(newStr1)
            temp[newStr2] = self.fitness_function(newStr2)

        if popLen % 2 == 1:
            temp.update({list(temp.items())[0][0]: list(temp.items())[0][1]})
        return temp

    def mutation(self, children):
        temp = {}
        for key, value in children.items():
            rand = random.randint(1, 10)
            if rand >= 9:
                rand2 = random.randint(0, self.levelLen - 1)
                rand3 = random.randint(0, 2)
                l = list(key)
                l[rand2] = str(rand3)
                key = ''.join(l)
                value = self.fitness_function(key)
                key = list(key)
                for i in range(len(key)):
                    if key[i] == '1':
                        if i < len(key) - 1:
                            key[i + 1] = '0'
                key = ''.join(key)
                temp.update({key: value})
            else:
                temp.update({key: value})

        self.populationFitness = temp
        return temp

    def get_children(self):
        d1 = self.selection()
        d2 = self.crossover(deepcopy(d1))

        temp = d2

        self.populationFitness = temp

        return temp

    def get_initialPopulation(self):
        return self.initialPopulation

    def get_populationFitness(self):
        return self.populationFitness

    def run_algo(self, action):
        g = Game(levels=self.level)
        g.load_next_level()
        point = g.get_score(action)
        return point

    def get_point(self):
        temp = deepcopy(self.populationFitness)
        score = 0
        for key, value in temp.items():
            score += value
        return score / len(temp)

    def get_max_point(self):
        temp = deepcopy(self.populationFitness)
        temp = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)}
        return list(temp.items())[0][1]

    def get_min_point(self):
        temp = deepcopy(self.populationFitness)
        temp = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1])}
        return list(temp.items())[0][1]

    def do_algo(self):
        for i in range(1000000):
            a = self.mutation(self.get_children())
            print(a)
            print(self.get_point())

            self.minFitness.append(self.get_min_point())
            self.avgFitness.append(self.get_point())
            self.maxFitness.append(self.get_max_point())

            if self.run_algo(list(a.items())[0][0])[0]:
                visualaize = Visualize(self.level[0], list(a.items())[0][0])
                visualaize.render()
                print(i)
                plt.plot(self.maxFitness)
                plt.plot(self.avgFitness)
                plt.plot(self.minFitness)
                plt.show()
                exit()


# g = Genetic(["_G___M_____LL_____G__G______L_____G____MM___G_G____LML____G___L____LMG___G___GML______G____L___MG___"],
#             500, 100, 0.1, 50, False, False)
# g.initial_population()
# # print(g.get_initialPopulation())
# # print(g.get_populationFitness())
# # print(g.selection())
# # a = g.get_children()
# # print(g.mutation(a))
# g.do_algo()
