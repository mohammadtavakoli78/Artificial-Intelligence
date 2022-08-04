import collections
import main


class CSP:  # define CSP class
    def __init__(self, base):           # define constructor
        self.base = base                # initial base
        self.assignment = []            # define an array for assignment
        self.lenAssignment = 0          # define a variable for length of assignment
        self.finalAssignment = []       # define an array for final assignment
        self.domains = []               # define an array for domains of variables that can have
        self.backtrackAssignment = []   # define an array for backtrack assignment
        self.queue = []                 # define an array for MAC
        self.option = 0                 # if option is 0 we will have forward checking else it will be MAC
        self.step = 0                   # define a variable for number of steps

    def initialAssignment(self):        # this method updates assignment and domains of variables
        for row, l in enumerate(self.base):
            for column, item in enumerate(l):
                if item == '-':
                    temp = [row, column, item]
                    self.assignment.append(temp)    # append variables that have no value to assignment array
                    self.lenAssignment += 1
                    if self.tellConstraint(row, column) == 0 or self.tellConstraint(row, column) == 1:
                        self.domains.append([row, column, 1, self.tellConstraint(row, column)])
                    else:
                        self.domains.append([row, column, 2, -1])

    def checkFailure(self):     # this method checks if we observe rules of the game or not
        rows = []
        columns = []
        for i in self.base:     # get rows that all of it's home is full
            temp = ''
            for j in i:
                temp += j
            if '-' not in temp:
                rows.append(temp)
        for i in range(len(self.base[0])):      # get columns that all of it's home is full
            temp = ''
            for j in range(len(self.base[0])):
                temp += self.base[j][i]
            if '-' not in temp:
                columns.append(temp)
        dr = [item for item, count in collections.Counter(rows).items() if count > 1]
        rd = [item for item, count in collections.Counter(columns).items() if count > 1]
        if len(dr) > 0 or len(rd) > 0:      # check don't have same string in all rows and columns
            return False

        for i in rows:      # enumerate number of 1 and 0 in each row
            zero = 0
            one = 0
            for j in i:
                if j == '0':
                    zero += 1
                elif j == '1':
                    one += 1
            if zero != one:     # check number of 1 and 0 in each row and column be same
                return False

        for i in columns:       # enumerate number of 1 and 0 in each column
            zero = 0
            one = 0
            for j in i:
                if j == '0':
                    zero += 1
                elif j == '1':
                    one += 1
            if zero != one:     # check number of 1 and 0 in each row and column be same
                return False

        flag = False
        for row, i in enumerate(self.base):     # check don't have more that two 0 or 1 in each row or column
            for column, j in enumerate(i):
                if column > 1:
                    if self.base[row][column - 2] == self.base[row][column - 1] == self.base[row][column] and self.base[row][column] != '-':
                        flag = True
                if column < len(self.base[0]) - 3:
                    if self.base[row][column + 2] == self.base[row][column + 1] == self.base[row][column] and self.base[row][column] != '-':
                        flag = True
                if 0 < column < len(self.base[0]) - 2:
                    if self.base[row][column - 1] == self.base[row][column + 1] == self.base[row][column] and self.base[row][column] != '-':
                        flag = True
                if row > 1:
                    if self.base[row - 2][column] == self.base[row - 1][column] == self.base[row][column] and self.base[row][column] != '-':
                        flag = True
                if row < len(self.base[0]) - 3:
                    if self.base[row + 2][column] == self.base[row + 1][column] == self.base[row][column] and self.base[row][column] != '-':
                        flag = True
                if 0 < row < len(self.base[0]) - 2:
                    if self.base[row - 1][column] == self.base[row + 1][column] == self.base[row][column] and self.base[row][column] != '-':
                        flag = True
        if flag:
            return False

        return True

    def tellConstraint(self, row, column):      # this method tells in square that don't have any values
        temp = 0                                # which of 0, 1, or both can be placed
        zero = 0
        one = 0
        for i in self.base[row]:                # enumerate number of 0 and 1 in rows
            if i != '-':
                temp += 1
                if i == '0':
                    zero += 1
                elif i == '1':
                    one += 1
        if temp == len(self.base[row]) - 1:
            if zero > one:
                return 1
            else:
                return 0
        temp = 0
        zero = 0
        one = 0
        for i in range(0, len(self.base[row])):     # enumerate number of 0 and 1 in columns
            if self.base[i][column] != '-':
                temp += 1
                if i == '0':
                    zero += 1
                elif i == '1':
                    one += 1
        if temp == len(self.base[row]) - 1:
            if zero > one:
                return 1
            else:
                return 0
        if 0 < column < len(self.base[row]) - 1:        # check if we have n - 1 variables in each rows and columns
            if self.base[row][column - 1] == self.base[row][column + 1]:
                if self.base[row][column - 1] == '0':
                    return 1
                elif self.base[row][column - 1] == '1':
                    return 0
        if 0 < row < len(self.base[row]) - 1:
            if self.base[row - 1][column] == self.base[row + 1][column]:
                if self.base[row - 1][column] == '0':
                    return 1
                elif self.base[row - 1][column] == '1':
                    return 0
        if 1 < column:
            if self.base[row][column - 2] == self.base[row][column - 1]:
                if self.base[row][column - 1] == '0':
                    return 1
                elif self.base[row][column - 1] == '1':
                    return 0
        if 1 < row:
            if self.base[row - 2][column] == self.base[row - 1][column]:
                if self.base[row - 1][column] == '0':
                    return 1
                elif self.base[row - 1][column] == '1':
                    return 0
        if column < len(self.base[row]) - 3:
            if self.base[row][column + 2] == self.base[row][column + 1]:
                if self.base[row][column + 1] == '0':
                    return 1
                elif self.base[row][column + 1] == '1':
                    return 0
        if row < len(self.base[row]) - 3:
            if self.base[row + 2][column] == self.base[row + 1][column]:
                if self.base[row + 1][column] == '0':
                    return 1
                elif self.base[row + 1][column] == '1':
                    return 0
        return 2

    def backtrack(self):            # this method runs backtrack algorithm
        if self.goalTest():
            return True
        a = self.MRV()
        b = [0, 1]
        for i in b:
            self.base[a[0]][a[1]] = str(i)
            self.finalAssignment.append([a[0], a[1], str(i)])
            self.step += 1
            if self.option == 0:                    # this condition runs forward checking
                self.forwardChecking()
            else:                                   # this condition runs MAC
                tempDomain = []
                keyValue = 0
                for key, i in enumerate(self.domains):
                    if str(i[0]) == str(a[0]) and str(i[1]) == str(a[1]):
                        tempDomain = i
                        keyValue = key
                del self.domains[keyValue]
                if a[1] > 0:
                    if self.base[a[0]][a[1] - 1] == '-':
                        self.queue.append([[a[0], a[1]], [a[0], a[1] - 1]])
                if a[1] < len(self.base[0]) - 1:
                    if self.base[a[0]][a[1] + 1] == '-':
                        self.queue.append([[a[0], a[1]], [a[0], a[1] + 1]])
                if a[0] > 0:
                    if self.base[a[0] - 1][a[1]] == '-':
                        self.queue.append([[a[0], a[1]], [a[0] - 1, a[1]]])
                if a[0] < len(self.base[0]) - 1:
                    if self.base[a[0] + 1][a[1]] == '-':
                        self.queue.append([[a[0], a[1]], [a[0] + 1, a[1]]])
                self.MAC()

            if self.checkFailure():
                result = self.backtrack()
                if result:
                    return result
            self.base[self.finalAssignment[-1][0]][self.finalAssignment[-1][1]] = '-'
            if self.option == 1:
                # self.domains.append([self.finalAssignment[-1][0], self.finalAssignment[-1][1], 2, -1])
                self.domains.insert(0, [self.finalAssignment[-1][0], self.finalAssignment[-1][1], 2, -1])
            del self.finalAssignment[-1]
        return False

    def forwardChecking(self):                      # this method if forward-checking algorithm
        self.domains = []
        for row, l in enumerate(self.base):
            for column, item in enumerate(l):
                if item == '-':
                    if self.tellConstraint(row, column) == 0 or self.tellConstraint(row, column) == 1:
                        self.domains.append([row, column, 1, self.tellConstraint(row, column)])
                    else:
                        self.domains.append([row, column, 2, -1])

    def revise(self, dot1, dot2):                   # this method make two nodes arc-consistence
        flag = False
        change = False
        temp = self.base[dot2[0]][dot2[1]]
        tempDomain = []
        for i in self.domains:
            if str(i[0]) == str(dot1[0]) and str(i[1]) == str(dot1[1]):
                tempDomain = i
        if tempDomain[3] == 2 or (tempDomain[2] == 1 and tempDomain[3] == '0'):
            self.base[dot1[0]][dot1[1]] = '0'
            for i in [0, 1]:
                self.base[dot2[0]][dot2[1]] = str(i)
                if self.checkFailure():
                    flag = True
            if not flag:
                self.domains[dot1[0]][dot1[1]] = [dot1[0], dot1[1], 1, '1']
                change = True
            flag = False
        if tempDomain[3] == 2 or (tempDomain[2] == 1 and tempDomain[3] == '1'):
            self.base[dot1[0]][dot1[1]] = '1'
            for i in [0, 1]:
                self.base[dot2[0]][dot2[1]] = str(i)
                if self.checkFailure():
                    flag = True
            if not flag:
                self.domains[dot1[0]][dot1[1]] = [dot1[0], dot1[1], 0, -1]
                change = True
        self.base[dot1[0]][dot1[1]] = '-'
        self.base[dot2[0]][dot2[1]] = temp
        return change

    def MAC(self):                         # this method do MAC algorithm
        while len(self.queue) > 0:
            a = self.queue.pop()
            if self.revise(a[1], a[0]):
                if a[1][1] > 0:
                    if self.base[a[1][0]][a[1][1] - 1] == '-':
                        self.queue.append([[a[1][0], a[1][1]], [a[1][0], a[1][1] - 1]])
                if a[1][1] < len(self.base[0]) - 1:
                    if self.base[a[1][0]][a[1][1] + 1] == '-':
                        self.queue.append([[a[1][0], a[1][1]], [a[1][0], a[1][1] + 1]])
                if a[1][0] > 0:
                    if self.base[a[1][0] - 1][a[1][1]] == '-':
                        self.queue.append([[a[1][0], a[1][1]], [a[1][0] - 1, a[1][1]]])
                if a[1][0] < len(self.base[0]) - 1:
                    if self.base[a[1][0] + 1][a[1][1]] == '-':
                        self.queue.append([[a[1][0], a[1][1]], [a[1][0] + 1, a[1][1]]])

    def MRV(self):          # this method do MRV
        done = False
        for index, l in enumerate(self.domains):
            if l[2] == 1:
                done = True
                return [l[0], l[1]]

        if not done:
            return [self.domains[0][0], self.domains[0][1]]

    def LCV(self):
        pass

    def goalTest(self):             # this method checks backtrack algorithms is finished or not
        if len(self.finalAssignment) == self.lenAssignment:
            return True
        else:
            return False

    def printBase(self):            # this method print base
        print(self.base)

    def printAssignment(self):      # this method print assignment
        print(self.assignment)

    def printFinalAssignment(self):     # this method print final assignment
        print(self.finalAssignment)

    def runAlgorithm(self):             # this method runs backtrack algorithm and return answer
        self.backtrack()
        for i in self.base:
            for j in i:
                print(j, end=" ")
            print()
        if len(self.finalAssignment) == 0:
            print("Puzzle don't have any answer")


base = main.base
csp = CSP(base)
csp.initialAssignment()
csp.runAlgorithm()
# csp.printBase()
csp.printFinalAssignment()
print(csp.step)
