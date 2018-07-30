from Square import Square
from copy import deepcopy
import random

class Sudoku:
    def __init__(self):
        self.tab = None

    def createSudoku(self):
        """
        Create the sudoku (the answer)
        """
        self.tab = [[Square() for _ in range(3)] for _ in range(3)]
        self.makeCross()
        self.makeCoins()

    def makeFromDependancy(self, possibilities, isHorizontal):
        """
        This is the method that is going to create randomly the square with the possibilities it haves
        :param possibilities: int[] inside a 3x3 -> inside the int[] there is the numbers that can go in the spot of the square
        :param isHorizontal: if we want the matrix to be created from left to right or from top to bottom
        :return: the randomly correctly generated matrix
        """
        tempMatrix = [[0 for _ in range(3)] for _ in range(3)]
        done = False
        while not done:
            index = 0
            value_x, value_y = 0, 0
            tempPoss = deepcopy(possibilities)
            while index < 9 and len(tempPoss[value_x][value_y]) != 0:
                choice = (int)(random.random() * len(tempPoss[value_x][value_y]))
                tempMatrix[value_x][value_y] = tempPoss[value_x][value_y][choice]
                valueDelete = tempPoss[value_x][value_y][choice]
                for i in range(len(tempPoss)):
                    for j in range(len(tempPoss[i])):
                        if valueDelete in tempPoss[i][j]:
                            tempPoss[i][j].remove(valueDelete)
                index += 1
                if isHorizontal:
                    value_x, value_y = (int)((index - index % 3) / 3), index % 3
                else:
                    value_y, value_x = (int)((index - index % 3) / 3), index % 3

            if self.__finishedMatrix(tempMatrix):
                done = True
        return tempMatrix

    def createFromDependancy(self, square, isHorizontal):
        """
        Create a matrix from only one dependancy (it's to make the cross of the sudoku)
        :param square: The 3x3 matrix that is going to eliminate possibilities from the matrix you are trying to create
        :param isHorizontal: If the matrices are possitionned vertically or horizontally from one another
        :return: The 3x3 matrix you wanted to create
        """
        otherMatrix = deepcopy(square.tab)
        possibilities = [[[i for i in range(1,10)] for _ in range(3)] for _ in range(3)]

        #eliminate the possibilities that are in the same line as the otherMatrix
        self.eliminatePoss(otherMatrix, isHorizontal, possibilities)

        #fill the tempMatrix
        tempMatrix = self.makeFromDependancy(possibilities, isHorizontal)

        return tempMatrix

    def __finishedMatrix(self, matrix2d):
        """
        Verify if the 3x3 matrix is full
        :param matrix2d:The matrix you are trying to tcheck the fullness
        :return: if the matrix is full
        """
        for i in matrix2d:
            for j in i:
                if j == 0:
                    return False
        return True

    def eliminatePoss(self, matrix, isHorizontal, possibilities):
        """
        This is meant to see what numbers are still available for a matrix (by elimating numbers from the possibilities matrix)
        :param matrix: The matrix that we don't want to have numbers in the same column/row
        :param isHorizontal: If those matrices are positionned horizontally or vertically from one another
        :param possibilities: int[] in a 3x3 matrix that enumerate the numbers that can be in a certain position
        """
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for k in range(len(possibilities[i])):
                    if isHorizontal:
                        if matrix[i][j] in possibilities[i][k]:
                            possibilities[i][k].remove(matrix[i][j])
                    else:
                        if matrix[i][j] in possibilities[k][j]:
                            possibilities[k][j].remove(matrix[i][j])

    def switch(self, number, notTouch, twinIndex):
        """
        Switch the position of the number that is a problem with the creation of the middle square with another one

        The problem refers to the middle having a place with no possibilities because at some other place 2 numbers must be there (the 2 numbers are entangled -> look at the image for more clarification)
        :param number: the number that is creating the problem
        :param notTouch: The other number that is creating the problem
        :param twinIndex:
        :return:
        """
        matrices = [self.tab[twinIndex[0][0]][twinIndex[0][1]].tab, self.tab[twinIndex[1][0]][twinIndex[1][1]].tab]

        #choose anotherNumber to switch with
        poss = [i for i in range(1,10)]
        poss.remove(number)
        poss.remove(notTouch)
        anotherNumber = poss[(int)(random.random()*len(poss))]

        #find the index of the numbers
        indexes = [[[0 for _ in range(2)] for _ in range(2)] for _ in range(2)] # Matrices -> number , anotherNumber -> the position
        for i in range(len(matrices)):
            for j in range(len(matrices[i])):
                for k in range(len(matrices[i][j])):
                    if matrices[i][j][k] == number:
                        indexes[i][0] = [j, k]
                    elif matrices[i][j][k] == anotherNumber:
                        indexes[i][1] = [j, k]

        #make the switch
        for i in range(2):
            matrices[i][indexes[i][0][0]][indexes[i][0][1]], matrices[i][indexes[i][1][0]][indexes[i][1][1]] = matrices[i][indexes[i][1][0]][indexes[i][1][1]], matrices[i][indexes[i][0][0]][indexes[i][0][1]]

    def complete(self, hori, verti):
        """
        This fonction will try to complete the square (if it is possible)
        :param hori: The indexed of the 2, 3x3, matrices that are positionned horizontally to the square you are trying to build
        :param verti: same as hori but positionned vertically
        :return: The 3x3 matrix or the 2 numbers that are posing a problem
        """
        possibilities = [[[i for i in range(1, 10)] for _ in range(3)] for _ in range(3)]
        for n in hori:
            tempMatrix = deepcopy(self.tab[n[0]][n[1]].tab)
            self.eliminatePoss(tempMatrix, True, possibilities)

        for n in verti:
            tempMatrix = deepcopy(self.tab[n[0]][n[1]].tab)
            self.eliminatePoss(tempMatrix, False, possibilities)

        for i in range(len(possibilities)):
            for j in range(len(possibilities[i])):
                if (len(possibilities[i][j]) > 1):
                    return possibilities[i][j]
        return possibilities

    def finalCompleteMatrix(self, hori, verti, indexReplaced):
        """
        This will try to make the square of the center
        :param hori: The indexed of the 2, 3x3, matrices that are positionned horizontally to the square you are trying to build
        :param verti: same as hori but positionned vertically
        :param indexReplaced: The index of the square in the middle (I made it with more parameters but ended up not using it)
        """
        tryMat = self.complete(hori, verti)

        while type(tryMat[0]) == int:
            indexStay = (int)(random.random() * 2)
            numberStay, numberChange = tryMat[indexStay], tryMat[(indexStay+1)%2]
            self.switch(numberChange, numberStay, verti if (int)(random.random()*2) else hori)
            tryMat = self.complete(hori, verti)

        for i in range(len(self.tab[indexReplaced[0]][indexReplaced[1]].tab)):
            for j in range(len(self.tab[indexReplaced[0]][indexReplaced[1]].tab[i])):
                self.tab[indexReplaced[0]][indexReplaced[1]].tab[i][j] = tryMat[i][j][0]

    def makeCross(self):
        """
        Make all the squares except for the corners
        """
        self.tab[0][1].initTabRand()
        self.tab[1][0].initTabRand()
        self.tab[2][1].tab = self.createFromDependancy(self.tab[0][1], False)
        self.tab[1][2].tab = self.createFromDependancy(self.tab[1][0], True)
        self.finalCompleteMatrix([[1,0], [1,2]], [[0,1], [2,1]], [1,1])

    def findIndex(self, index, number):
        """
        This is for finding the position of a number from a matrix
        :param index: This is the position of the matrix in the sudoku
        :param number: This is the number we are looking for
        :return: The index of the number
        """
        for i in range(3):
            for j in range(3):
                if self.tab[index[0]][index[1]].tab[i][j] == number:
                    return [i,j]

    def othersInLine(self, indexMatrix, indexNumber, isHorizontal):
        """
        See the other numbers that can be switched
        :param indexMatrix:The matrix we want to switch the numbers
        :param indexNumbers: The index of the number inside the matrix
        :param isHorizontal: do we want a horizontal switch or a vertical one
        :return: the others that are in the line of the number
        """
        others = []
        cote = 3

        for i in range(cote):
            if isHorizontal and i != indexNumber[1]:
                others.append(self.tab[indexMatrix[0]][indexMatrix[1]].tab[indexNumber[0]][i])
            elif not isHorizontal and i != indexNumber[0]:
                others.append(self.tab[indexMatrix[0]][indexMatrix[1]].tab[i][indexNumber[1]])
        return others

    def blindChanging(self, hori, verti, index, last):
        """
        This will try to switch the numbers in the corners and vertically or horizontally in the semi-middles (so that it does not change the middle) and print the final sudoku
        :param hori: a 2z2 array that tells us the indexes of the 2 squares that are horizontal to the one we are trying to make
        :param verti:a 2x2 array that tell us the indexed of the 2 sqaures that are vertical to the one we are trying to make
        :param index: the position of the square we are trying to make in this.tab
        """
        tryMat = self.complete(hori, verti)
        if type(tryMat[0]) == int:
            #These will become 4x2 matrices 4 (numb1 M1, numb1 M2, numb2 M1, numb2 M2)(numb => number / M=> matrix); the 2 is from the position
            horiIndex = []
            vertiIndex = []

            for i in range(2): #the matrix
                for j in range(2): #The number we are looking for
                    horiIndex.append(self.findIndex(hori[j], tryMat[i]))
                    vertiIndex.append(self.findIndex(verti[j], tryMat[i]))

            tempOthers = []

            tempOthers.append([])
            for i in range(len(horiIndex)):
                if i%2 == 0:
                    tempOthers[0].append([])
                tempOthers[0][(int) (i/2)].append(self.othersInLine(hori[i%2], horiIndex[i], False))

            tempOthers.append([])
            for i in range(len(vertiIndex)):
                if i%2 == 0:
                    tempOthers[1].append([])
                tempOthers[1][(int) (i/2)].append(self.othersInLine(verti[i%2], vertiIndex[i], True))

            pos_try = []
            pos_found = []
            isHorizontal = None

            for i in range(2): # horizontal -> vertical
                for j in range(2): # first number of tryMat -> second number of tryMat
                    for k in range(2):
                        if tempOthers[i][j][0][k] in tempOthers[i][j][1] and tempOthers[i][j][0][k] not in tryMat and len(pos_try) + len(pos_found) == 0:
                            if i == 0: # horizontal
                                isHorizontal = True
                                pos_try.append(horiIndex[j*2])
                                pos_try.append(horiIndex[1 + j*2])

                                pos_found.append(self.findIndex(hori[0], tempOthers[i][j][0][k]))
                                pos_found.append(self.findIndex(hori[1], tempOthers[i][j][0][k]))


                            else: #vertical
                                isHorizontal = False
                                pos_try.append(vertiIndex[j*2])
                                pos_try.append(vertiIndex[1 + j*2])

                                pos_found.append(self.findIndex(verti[0], tempOthers[i][j][0][k]))
                                pos_found.append(self.findIndex(verti[1], tempOthers[i][j][0][k]))

            if len(pos_try) + len(pos_found) == 0 or [pos_try, pos_found] in last:
                self.createSudoku()
            else:
                if isHorizontal:
                    for i in range(2):
                        self.tab[hori[i][0]][hori[i][1]].tab[pos_found[i][0]][pos_found[i][1]],\
                        self.tab[hori[i][0]][hori[i][1]].tab[pos_try[i][0]][pos_try[i][1]] = \
                        self.tab[hori[i][0]][hori[i][1]].tab[pos_try[i][0]][pos_try[i][1]], \
                        self.tab[hori[i][0]][hori[i][1]].tab[pos_found[i][0]][pos_found[i][1]]

                else:
                    for i in range(2):
                        self.tab[verti[i][0]][verti[i][1]].tab[pos_found[i][0]][pos_found[i][1]], \
                        self.tab[verti[i][0]][verti[i][1]].tab[pos_try[i][0]][pos_try[i][1]] = \
                        self.tab[verti[i][0]][verti[i][1]].tab[pos_try[i][0]][pos_try[i][1]], \
                        self.tab[verti[i][0]][verti[i][1]].tab[pos_found[i][0]][pos_found[i][1]]
                last.append([pos_try, pos_found])
                self.blindChanging(hori, verti, index, last)


        else:
            print("Done \n")
            for i in range(len(tryMat)):
                for j in range(len(tryMat[i])):
                    self.tab[index[0]][index[1]].tab[i][j] = tryMat[i][j][0]
            self.afficherTout()

    def possible(self, poss):
        """
        See if it is possible to make the matrix (if their is no more possibilities it's impossible)
        :param poss: int[3][3] -> int[] for the possibilities from 1 to 9 (so basically 3d)
        :return: If it is possible to complete
        """
        for i in poss:
            for j in i:
                if len(j) == 0:
                    return False
        return True

    def makeCoins(self):
        """
        This will make the corners
        """
        coinsPoss = [[[[i for i in range(1,10)] for _ in range(3)] for _ in range(3)] for _ in range(4)]
        coinsIndex = [[0,0], [0,2], [2,0], [2,2]]
        for i in range(len(coinsIndex)):
            self.eliminatePoss(self.tab[coinsIndex[i][0]][1].tab, True, coinsPoss[i])
            self.eliminatePoss(self.tab[1][coinsIndex[i][1]].tab, False, coinsPoss[i])

        self.tab[0][0].tab = self.makeFromDependancy(coinsPoss[0], (int)(random.random() * 2) == 0)

        continuer = True
        for i in range(1,3):
            self.eliminatePoss(self.tab[0][0].tab, i%2 == 1, coinsPoss[i])
            if not self.possible(coinsPoss[i]):
                continuer = False
                self.createSudoku()
            else:
                self.tab[coinsIndex[i][0]][coinsIndex[i][1]].tab = self.makeFromDependancy(coinsPoss[i], (int)(random.random() * 2) == 0)

        # Works until now :)
        if continuer:
            self.blindChanging([[2,0],[2,1]],[[0,2], [1,2]], [2,2], [])

    def afficherTout(self):
        for i in range(3):
            for i2 in range(3):
                messageLine = ""
                for j in range(3):
                    for j2 in range(3):
                        temp = str(self.tab[i][j].tab[i2][j2]) if self.tab[i][j].tab[i2][j2] is not None else " "
                        messageLine += temp + "  " + ("  " if j2 % 3 == 2 else "")
                print(messageLine)
                if i2%3 == 2:
                    print("")
        print("")

    def findPosProb(self):
        """
        This is used to delete numbers but in a semi-random way (to try to avoid as much as possible having completly filled squares and square that are empty)
        :return: The possition of the number to delete
        """
        numb_total = sum(sum(sum(sum(0 if self.tab[i][j].tab[k][l] is None else 1 for i in range(3)) for j in range(3)) for k in range(3)) for l in range(3))
        index = (int)(random.random() * numb_total)
        numb = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if self.tab[i][j].tab[k][l] is not None:
                            if numb == index:
                                return [i,j,k,l]
                            numb += 1



    def finalSudoku(self):
        """
        This will print the sudoku that the user will see when he or she plays the game
        """
        number_delete = 40

        number = 0
        while number < number_delete:
            pos = self.findPosProb()
            if self.tab[pos[0]][pos[1]].tab[pos[2]][pos[3]] is not None:
                self.tab[pos[0]][pos[1]].tab[pos[2]][pos[3]] = None
                number += 1
        self.afficherTout()

temp = Sudoku() #creates the instance
temp.createSudoku() #creates the answer
temp.finalSudoku() #creates the "playable" sudoku




