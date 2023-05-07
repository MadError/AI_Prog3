from random import randint
import random
from math import isqrt

#random.seed(10)
# mark on the hints accoriding to given mine coordinate
def return_hint(map, mine_coor, size1, size2):
    for x,y in mine_coor:
        # if x or y has exceed to boundary
        x_a = (x+1 < size1)
        y_a = (y+1 < size2)
        x_m = (x-1 >= 0)
        y_m = (y-1 >= 0)

        if x_m and y_m and map[x-1][y-1] != 'x':
            map[x-1][y-1] += 1
        if x_m and map[x-1][y] != 'x':
            map[x-1][y] += 1
        if x_m and y_a and map[x-1][y+1] != 'x':
            map[x-1][y+1] += 1

        if y_m and map[x][y-1] != 'x':
            map[x][y-1] += 1
        if y_a and map[x][y+1] != 'x':
            map[x][y+1] += 1

        if x_a and y_m and map[x+1][y-1] != 'x':
            map[x+1][y-1] += 1
        if x_a and map[x+1][y] != 'x':
            map[x+1][y] += 1
        if x_a and y_a and map[x+1][y+1] != 'x':
            map[x+1][y+1] += 1

class game_board:
    def __init__(self, size1, size2, mine_num):
        self.size1 = size1
        self.size2 = size2
        self.mine_num = mine_num
        self.mine_coor = []
        self.map = [[0]*size2 for _ in range(size1)]

        # game map setup
        self.mine_coor = []
        while len(self.mine_coor) != self.mine_num:
            x, y = randint(0,self.size1-1), randint(0,self.size2-1)
            if (x,y) in self.mine_coor:
                continue
            self.mine_coor.append((x,y))
        
        # mark mine
        for x,y in self.mine_coor:
            self.map[x][y] = 'x'

        # mark hint
        return_hint(self.map, self.mine_coor, self.size1, self.size2)

    # return hint
    def query(self, x, y):
        return self.map[x][y]
    
    # randomly return sqrt(#cells) safe
    def init_safe(self):
        safe = []
        safe_length = isqrt(self.size1*self.size2)
        while safe_length:
            x, y = randint(0,self.size1-1), randint(0,self.size2-1)
            if (x, y) in safe or (x, y) in self.mine_coor:
                continue
            safe.append([((x, y), 0)])
            safe_length -= 1
        return safe
    
    def check(self, map):
        for m in map:
            if self.map[m[0][0]][m[0][1]] == 'x' and m[1] == 0:
                return 0
            if self.map[m[0][0]][m[0][1]] != 'x' and m[1] == 1:
                return 0
        return 1
