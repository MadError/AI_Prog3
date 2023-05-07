from mine_game import game_board
from itertools import combinations
import copy

def subset(new_c):
    for k in KB:
        if all(i in new_c for i in k):
            return 1
        elif all(i in k for i in new_c):
            KB.remove(k)
            return 0
    return 0

def insert(new_c):
    if new_c and len(new_c) != 1:
        for k in KB0:
            if new_c:
                new_c = KB0_match(k, new_c)
            else:
                break

    if not new_c or new_c in KB or subset(new_c):
        return 0
    
    KB.append(new_c)
    return 1

def return_mark(x, y):
    for k in KB0:
        if (x,y) == k[0]:
            return k[1]
    return -1

def generate_from_hint(x, y, hint):
    unmark, mine = process_hint(x,y)
    if not unmark:
        return
    left = len(unmark)
    # pos
    if hint-mine > 0:
        combs = combinations(unmark, (left-hint+mine+1))
        for com in combs:
            clause = []
            for c in com:
                clause.append((c,1))
            insert(clause)
    # neg
    if left > hint-mine:
        combs = combinations(unmark, (hint-mine+1))
        for com in combs:
            clause = []
            for c in com:
                clause.append((c,0))
            insert(clause)

def process_hint(x, y):
    unmark = []
    mine = 0
    x_a = (x+1 < size1)
    y_a = (y+1 < size2)
    x_m = (x-1 >= 0)
    y_m = (y-1 >= 0)

    if x_m and y_m:
        mark = return_mark(x-1,y-1)
        if mark == -1:
            unmark.append((x-1,y-1))
        elif mark:
            mine += 1
    if x_m:
        mark = return_mark(x-1,y)
        if mark == -1:
            unmark.append((x-1,y))
        elif mark:
            mine += 1
    if x_m and y_a:
        mark = return_mark(x-1,y+1)
        if mark == -1:
            unmark.append((x-1,y+1))
        elif mark:
            mine += 1

    if y_m:
        mark = return_mark(x,y-1)
        if mark == -1:
            unmark.append((x,y-1))
        elif mark:
            mine += 1
    if y_a:
        mark = return_mark(x,y+1)
        if mark == -1:
            unmark.append((x,y+1))
        elif mark:
            mine += 1

    if x_a and y_m:
        mark = return_mark(x+1,y-1)
        if mark == -1:
            unmark.append((x+1,y-1))
        elif mark:
            mine += 1
    if x_a:
        mark = return_mark(x+1,y)
        if mark == -1:
            unmark.append((x+1,y))
        elif mark:
            mine += 1
    if x_a and y_a:
        mark = return_mark(x+1,y+1)
        if mark == -1:
            unmark.append((x+1,y+1))
        elif mark:
            mine += 1

    return unmark, mine

def KB0_match(clau1, clau2):
    if clau1 in clau2:
        return None
    elif (clau1[0],int(not clau1[1])) in clau2:
        clau2.remove((clau1[0],int(not clau1[1])))
        return clau2
    else:
        return clau2

def match(clau1, clau2):
    if clau2 not in KB:
        return
    if len(clau1) == 1:
        if clau1[0] in clau2:
            KB.remove(clau2)
            return None
        elif (clau1[0][0],int(not clau1[0][1])) in clau2:
            KB.remove(clau2)
            clau2.remove((clau1[0][0],int(not clau1[0][1])))
            return clau2
        else:
            return None

    new_flag = False
    c = clau1 + [c2 for c2 in clau2 if c2 not in clau1]
    for c1 in clau1:
        for c2 in clau2:
            if c1[0] == c2[0] and c1[1] != c2[1]:
                if new_flag:
                    return None
                new_flag = True
                c.remove(c1)
                c.remove(c2)

    return c if new_flag else None
    

def single_literal(kb):
    # return the first idx of single-literal in kb
    for i,clause in enumerate(kb):
        if len(clause) == 1:
            return i, clause
    return -1, None

if __name__ == '__main__':
    size1 = 16
    size2 = 30
    pause_flag = 0
    game = game_board(size1,size2,25)
    KB = game.init_safe()
    KB0 = []

    while KB and pause_flag < 5:
        pause_flag += 1
        single, clause = single_literal(KB)
        
        if single != -1:
            # append to KB0
            del KB[single]
            KB0.append(clause[0])
            pause_flag = 0
            # match with other clauses
            KB_loop = KB.copy()
            for k in KB_loop:
                new_c = match(clause, k)
                insert(new_c)
            # query hint and append new clauses
            if clause[0][1] == 1:
                continue
            hint = game.query(clause[0][0][0], clause[0][0][1])
            generate_from_hint(clause[0][0][0], clause[0][0][1], hint)
        else:
            for i,k1 in enumerate(KB[:-1]):
                if len(k1) > 2:
                    continue
                for k2 in KB[i+1:]:
                    if len(k2) > 2:
                        continue
                    new_c = match(k1, k2)
                    insert(new_c)


    print('len:',len(KB0))
    print('len:',len(KB))
    print('flag:', pause_flag)

    print(game.check(KB0))

