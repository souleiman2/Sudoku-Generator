import random
class Square:
    def __init__(self):
        """
        Constructor of the square
        """
        self.COTE = 3
        self.tab = [[0 for _ in range(self.COTE)] for _ in range(self.COTE)]
        self.possibilities = [i for i in range(1,10)]
        self.available = [i for i in range(1,10)]

    def initTabRand(self):
        """
        Fill the square randomly
        """
        for i in range(self.COTE):
            for j in range(self.COTE):
                index = (int)(random.random()*len(self.available))
                self.tab[i][j] = self.available[index]
                self.available.pop(index)

