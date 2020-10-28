""" Domain API for the Pacman game project """

import random

# def loadMaze(fname):
    # Maze = []
    # f = open(fname)
    # lines = f.readlines()
    # for line in lines :
        # m = line.strip('\n').split('\t')
        # Maze.append(m)
    # f.close()
    # return Maze

def new_game1(num) :

    L= [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,2],
        [2,0,1,1,1,1,1,1,1,1,2,0,2,0,2,0,2,0,2,0,2,0,2],
        [2,0,0,0,2,0,0,0,2,0,2,0,0,0,2,0,2,0,0,0,2,0,2],
        [2,1,1,0,2,0,2,0,2,0,2,1,1,1,2,0,2,1,2,0,2,0,2],
        [2,0,0,0,2,0,2,0,2,0,0,0,2,0,0,0,0,0,2,0,2,0,2],
        [2,0,2,1,2,0,2,0,2,0,2,0,2,0,2,0,1,1,2,0,2,0,2],
        [2,0,2,0,2,0,2,0,0,0,2,0,2,0,2,0,0,0,2,0,2,0,2],
        [2,0,2,0,2,0,2,1,2,0,2,1,2,0,2,0,2,0,2,0,2,0,2],
        [2,0,0,0,0,0,2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,2],
        [2,1,1,1,2,0,2,0,2,1,1,1,1,1,1,1,1,0,2,0,2,0,2],
        [2,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2],
        [2,1,1,0,2,0,1,1,1,0,2,0,1,1,1,0,2,0,2,0,0,0,2],
        [2,0,0,0,0,0,2,0,0,0,2,0,0,0,2,0,2,0,2,0,2,0,2],
        [2,1,1,1,1,1,1,"E",1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]
    
    count = 0
    while count < 5:             #randomly generated slippery positions
        m = random.randint(1,len(L)-1)
        n = random.randint(1,len(L[0])-1)
        if L[m][n] == 0 :
            L[m][n] = 3
            count += 1

    ghosts = []
    for i in range(num):         #randomly generated ghosts
        ghosts.append(ghost(L))

    return L, ghosts

def new_game2(num):

    L= [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [2,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,2],
        [2,0,2,0,2,0,2,0,2,0,2,0,2,0,1,1,2,0,2,0,1,1,1,1,1,1,1,1,2,0,2,0,2],
        [2,0,2,0,2,0,2,0,0,0,2,0,2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,2],
        [2,0,2,0,2,0,2,1,1,1,1,1,2,0,2,0,2,1,1,1,1,0,2,0,2,0,2,0,2,1,1,1,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,2,0,0,0,2,0,2,0,2,0,0,0,2,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,0,2,1,1,1,1,0,2,0,2,1,2,0,2,0,2,0,2,0,2,0,2],
        [2,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2,0,0,0,2,0,2,0,2],
        [2,0,2,0,2,1,1,1,1,1,1,1,2,0,2,1,1,1,1,0,2,0,2,0,2,1,2,0,2,1,2,0,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,2],
        [2,0,2,1,1,1,1,1,1,1,1,1,1,1,2,0,1,1,1,1,1,1,2,0,2,0,2,1,1,1,1,1,2],
        [2,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,2],
        [2,0,2,0,2,1,1,1,2,0,2,1,1,0,2,1,1,0,2,1,1,0,2,1,1,1,1,0,2,0,1,1,2],
        [2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,0,0,2],
        [2,0,2,0,2,0,2,0,2,0,2,0,2,0,2,0,0,0,2,0,2,0,2,0,2,0,1,1,2,0,2,0,2],
        [2,0,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1,1,2,0,2,0,2,0,2,0,0,0,2,1,2,0,2],
        [2,0,2,0,2,1,2,0,2,1,1,1,2,0,2,0,2,0,2,0,2,0,1,1,1,1,2,0,2,0,2,0,2],
        [2,0,0,0,2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,0,0,2,0,0,0,2,0,2],
        [2,1,1,1,2,0,1,1,2,0,1,1,1,1,2,0,2,0,2,1,1,1,1,1,2,0,2,0,2,0,2,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,0,0,2],
        [2,0,1,1,1,1,1,1,1,1,1,1,1,0,2,0,2,1,1,0,2,0,2,0,2,1,1,1,1,1,1,1,2],
        [2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,2],
        [2,0,2,0,2,0,2,1,2,0,2,1,0,1,2,0,2,0,2,0,2,1,1,0,2,0,2,0,1,1,2,0,2],
        [2,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,2,0,0,0,0,0,2,0,0,0,0,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,"E",1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]

    count = 0
    while count < 5:          #randomly generated slippery positions
        m = random.randint(1,len(L)-1)
        n = random.randint(1,len(L[0])-1)
        if L[m][n] == 0:
            L[m][n] = 3
            count += 1

    ghosts = []
    for i in range(num):         #randomly generated ghosts
        ghosts.append(ghost(L))
    return L, ghosts

class ghost:
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]

    def __init__(self, L):
        # 0: i++(go down), 1: j++ (go right), 2:i--(go top), 3: j-- (go left)
        self.dir = random.randint(0,3)
        m, n = 0, 0
        while L[m][n] != 0:
            m = random.randint(1,len(L)-1)
            n = random.randint(1,len(L[0])-1)
        L[m][n] = 'X'
        self.row = m
        self.col = n

    def move(self, go, L):
        L[self.row][self.col] = 0
        self.row += self.directionsDic[go][0]
        self.col += self.directionsDic[go][1]
        L[self.row][self.col] = 'X'

def randomGhostAction(L, ghost):
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
    dir = ghost.dir
    i = ghost.row
    j = ghost.col
    nextI = i + directionsDic[dir][0]
    nextJ = j + directionsDic[dir][1]
    if isValid(L, nextI, nextJ):
        return dir
    randomList =[]
    for a in range(4):
        if(a != dir):
            randomList.append(a)
    random.shuffle(randomList)
    for a in range(len(randomList)):
        dir = randomList[a]
        nextI = i + directionsDic[dir][0]
        nextJ = j + directionsDic[dir][1]
        if isValid(L, nextI, nextJ):
            return dir
    print()
    print("should never reach here, Reaching here means we have a poor ghost in a dead corner")
    print()

def eclideanGhostAction(i, j, pos_i, pos_j):
    dir = [[1,0], [0,1], [-1,0], [0.-1]]
    distance = []
    for n in range(4):
        i = i + dir[n][0]
        j = j + dir[n][1]
        if L[i][j] != 1 or L[i][j] != 2:
            dis = ((pos_i - i)**2 + (pos_j - j)**2)**(1/2)
            distance.append(dis)
    minDis = min(distance)
    return distance.index(minDis)

def manhanttanGhostAction(i, j, pos_i, pos_j):
    dir = [[1,0], [0,1], [-1,0], [0.-1]]
    distance = []
    for n in range(4):
        i = i + dir[n][0]
        j = j + dir[n][1]
        if L[i][j] != 1 or L[i][j] != 2:
            dis = abs(pos_i - i) + abs(pos_j - j)
            distance.append(dis)
    minDis = min(distance)
    return distance.index(minDis)

def isValid(L, i, j):
    if i<0 or j<0 or i >= len(L) or j>= len(L[0]):
        return False

    return L[i][j] == 0

def instruction() :    #function to show instructions 
    print()
    print("""Instructions:
    Use the W,A,S,D keys to move. You can only move one space at a time.
    Press w to move up. Press s to move down. Press a to move left. Press d to move right.
    Press e to exit game.
    Make your way through the maze. Try not to run into ghosts.""")

def wall() :           #function when bumping into a wall
    print()
    print("Oops! Ran into a wall! Try again!")
    print()

def slippery() :       #function when going into slippery position
    n = random.randint(0, 4)
    if n == 0 :        #25% chance that the action failed
        print("Oops! You slipped! Try again!")
        return True
    else :
        return False

def exit_game(L) :     #function to exiting the game
    print("Are you sure you want to leave the game?")
    sure = input("Y/N")
    if sure.lower() == "y" :
        return 1  
    elif sure.lower() == "n" :
        print("Okay! Feel free to explore!")

def win_game(score) :
    print()
    print("You Win!")
    print("You get total", score, "scores")

def lose_game(score):
    print("You bump into the ghosts!!")
    print("Oops, Game Over!")
    print("You get", score, "scores")

def maze(L, pos_i, pos_j) :           #function to show the maze
    for i in range(0, len(L)) :
        for j in range(0, len(L[0])) :
            if i == pos_i and j == pos_j :
                print("#", end=' ')
            elif L[i][j] == 0 :
                print(".", end=' ')      
            elif L[i][j] == 1 :
                print("-", end=' ')
            elif L[i][j] == 2:
                print("|", end=' ')
            elif L[i][j] == 3:
                print("*", end=' ')
            else:
                print(L[i][j], end=' ')
        print()

def play(L, pos_i, pos_j, move, score) :  #function to move the pacman
    while True :
        if L[pos_i][pos_j] != 3 :
            L[pos_i][pos_j] = " "
        
        if move.lower() == "w" :          #go up
            if L[pos_i-1][pos_j] in (1,2) :
                wall()
            elif L[pos_i-1][pos_j] == 3 :
                if(slippery()) :
                    pos_i -= 0
                else :
                    pos_i -= 1
            elif L[pos_i-1][pos_j] == "X" :
                lose_game(score)
                break
            else :
                pos_i -= 1
                score += 10
        
        elif move.lower() == "s" :        #go down
            if L[pos_i+1][pos_j] in (1,2) :
                wall()
            elif L[pos_i+1][pos_j] == 3 :
                if(slippery()) :
                    pos_i += 0
                else :
                    pos_i += 1
            elif L[pos_i+1][pos_j] == "X" :
                lose_game(score)
                break
            else :
                pos_i += 1
                score += 10
                
        elif move.lower() == "a" :        #go left
            if L[pos_i][pos_j-1] in (1,2) :
                wall()
            elif L[pos_i][pos_j-1] == 3 :
                if(slippery()) :
                    pos_j -= 0
                else :
                    pos_j -= 1
            elif L[pos_i][pos_j-1] == "X" :
                lose_game(score)
                break
            else:
                pos_j -= 1
                score += 10

        elif move.lower() == "d" :        #go right
            if L[pos_i][pos_j+1] in (1,2) :
                wall()
            elif L[pos_i][pos_j+1] == 3 :
                if(slippery()) :
                    pos_j += 0
                else :
                    pos_j += 1
            elif L[pos_i][pos_j+1] == "X" :
                lose_game(score)
                break
            else :
                pos_j += 1
                score += 10

        elif move.lower() == "e" :        #exit the game
            r = exit_game(L)
            if r == 1 :
                print("Bye!")
                break
        
        if L[pos_i][pos_j] == "E" :       #reach the exit and win the game
            maze(L,pos_i,pos_j)
            win_game(score)
            break

        for ghost in ghosts:
            bestAction = randomGhostAction(L,ghost)
            ghost.move(bestAction, L)
            if ghost.row == pos_i and ghost.col == pos_j:
                print("Oops, the ghost catches you!")
                print("you get", score, "scores")

        maze(L,pos_i,pos_j)
        print("You get", score, "scores")
        print()
        move = input("Enter an action ('w'=up, 's'=down, 'a'=left, 'd'=right, 'e'=exit):")
        print()

if __name__ == "__main__":
    while True:
        load = input("""Hello!
    1) Press 1 to choose small maze.
    2) Press 2 to choose big maze.
        """)
        ghostNum = int(input("Ha! How many ghosts do you want?"))
        score = 0
        if load == "1" :
            L, ghosts = new_game1(ghostNum)
            pos_i, pos_j = 7, 11
            break
        elif load == "2" :
            L, ghosts = new_game2(ghostNum)
            pos_i, pos_j = 14, 19
            break
        else :
            print("Oops! Did you want to say something else?")
    instruction()
    maze(L,pos_i,pos_j)
    print()
    move = input("Enter an action ('w'=up, 's'=down, 'a'=left, 'd'=right, 'e'=exit):")
    play(L,pos_i,pos_j,move, score)
