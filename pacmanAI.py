#Sub-sections of code:
#    1) Codes (functions) for saving, reopening or starting new game
#    2) Classes and imports
#    3) Functions
#    4) Functions for the two games
#    5) Introduction and initialisation
#    6) Code for movements
import random

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
        [2,1,1,1,2,0,2,0,2,1,1,1,1,1,1,1,1,1,1,0,2,0,2],
        [2,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2],
        [2,1,1,0,2,1,1,1,1,0,2,0,1,1,1,1,2,0,2,0,0,0,2],
        [2,0,0,0,0,0,2,0,0,0,2,0,0,0,2,0,2,0,2,0,2,0,2],
        [2,1,1,1,1,1,1,"E",1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]

    for i in range(5) :         #randomly generated slippery positions
        m = random.randint(1,len(L)-1)
        n = random.randint(1,len(L[0])-1)
        if L[m][n] == 0 :
            L[m][n] = 3

    ghosts = []

    for i in range(num):
        ghosts.append(ghost(L))

    return L, ghosts

def new_game2(num):

    L= [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [2,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,2],
        [2,0,2,0,2,0,2,0,2,0,2,0,2,0,1,1,2,0,2,0,1,1,1,1,1,1,1,1,2,0,2,0,2,0,2,0,2,0,2,0,2],
        [2,0,2,0,2,0,2,0,0,0,2,0,2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,2,0,2,0,0,0,2,0,2],
        [2,0,2,0,2,0,2,1,1,1,1,1,2,0,2,0,2,1,1,1,1,0,2,0,2,0,2,0,2,1,1,1,2,0,2,1,2,0,2,0,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,2,0,0,0,2,0,2,0,2,0,0,0,2,0,0,0,0,0,2,0,2,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,0,2,1,1,1,1,0,2,0,2,1,2,0,2,0,2,0,2,0,2,0,2,0,1,1,2,0,2,0,2],
        [2,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2,0,0,0,2,0,2,0,2,0,0,0,2,0,2,0,2],
        [2,0,2,0,2,1,1,1,1,1,1,1,2,0,2,1,1,1,1,0,2,0,2,0,2,1,2,0,2,1,2,0,2,0,2,0,2,0,2,0,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,2],
        [2,0,2,1,1,1,1,1,1,1,1,1,1,1,2,0,1,1,1,1,1,1,2,0,2,0,2,1,1,1,1,1,1,1,1,1,1,1,2,0,2],
        [2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2],
        [2,0,2,0,2,1,1,1,2,0,2,1,1,1,2,1,1,0,2,1,1,0,2,1,1,1,1,0,2,0,1,1,1,1,2,0,2,0,0,0,2],
        [2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,0,0,2,0,2,0,2,0,2,0,2],
        [2,0,2,0,2,0,2,0,2,0,2,0,2,0,2,0,0,0,2,0,1,2,2,0,2,0,1,1,2,1,2,0,2,0,2,0,2,0,2,0,2],
        [2,0,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1,1,2,0,1,2,2,0,2,0,1,1,2,1,2,0,2,0,2,0,2,0,2,0,2],
        [2,0,2,0,2,1,2,0,2,1,1,1,2,0,2,1,2,0,2,0,2,0,1,1,1,1,2,0,2,0,2,0,2,0,2,0,2,1,1,0,2],
        [2,0,0,0,2,0,0,0,2,0,0,0,0,0,2,0,2,0,2,0,2,0,0,0,0,0,2,0,2,0,2,0,2,0,0,0,2,0,0,0,2],
        [2,1,1,1,2,0,1,1,2,0,1,1,1,1,2,0,2,0,2,1,1,1,1,1,2,0,2,0,2,0,2,0,2,1,1,1,2,0,1,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,0,0,2,0,0,0,0,0,2,0,2],
        [2,0,0,1,1,1,1,1,1,1,1,1,1,0,2,0,2,1,1,0,2,0,2,0,2,1,1,1,1,1,1,1,1,1,1,0,2,0,2,0,2],
        [2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,2],
        [2,0,2,0,2,0,2,1,2,0,2,1,1,1,2,0,2,0,2,0,2,1,1,1,2,0,2,1,1,1,2,0,1,1,1,1,1,1,1,1,2],
        [2,0,2,0,2,0,2,0,2,0,2,0,0,0,2,0,0,0,2,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,2],
        [2,1,2,0,2,0,2,0,2,0,2,0,2,0,2,1,1,1,2,1,2,0,2,0,1,1,2,0,1,1,1,1,1,1,1,1,2,0,2,0,2],
        [2,0,0,0,2,0,0,0,2,0,0,0,2,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,0,0,2],
        [2,0,1,1,2,0,2,1,1,1,1,1,2,0,2,0,2,0,2,0,2,1,1,1,2,0,2,0,2,1,1,0,2,0,0,0,2,1,1,1,2],
        [2,0,0,0,2,0,2,0,0,0,0,0,2,0,0,0,2,0,2,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,2,0,0,0,0,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,"E",1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]

    for i in range(10):         #randomly generated slippery positions
        m = random.randint(1,len(L)-1)
        n = random.randint(1,len(L[0])-1)
        if L[m][n] == 0:
            L[m][n] = 3

    ghosts = []

    for i in range(num):
        ghosts.append(ghost(L))
    return L, ghosts

class ghost:
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]

    def __init__(self, L):
        # 0: i++(go bot), 1: j++ (go right), 2:i--(go top), 3: j-- (go left)
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


#FUNCTIONS
def spider_clusters() :       #function to define clusters of spiders
    s1 = [(19,1),(19,3),(20,2),(21,1),(21,3)]
    s2 = [(19,17),(19,18),(19,19),(20,19),(21,17),(21,18),(21,19)]
    s3 = [(11,37),(11,39),(12,38),(13,37),(13,39)]
    s4 = [(25,33),(25,35),(26,34),(27,33),(27,35)]
    s5 = [(37,17),(37,19),(38,18),(39,17),(39,19)]
    return s1,s2,s3,s4,s5
   
def wall() :        #function to warn about walls
    print()
    print("Oops! Ran into a wall! Try again!")
    print()

def isValid(L, i, j):
    if i<0 or j<0 or i >= len(L) or j>= len(L[0]):
        return False

    return L[i][j] == 0


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
    print("should never reach here, Reaching here means we have a poor ghost in a dead corner")



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
    return dir.index(minDis)

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
    return dir.index(minDis)




def slippery() :
    n = random.randint(0, 4)
    if n == 0 :     #25% chance that the action failed
        print("Oops! You slipped! Try again!")
        return True
    else :
        return False

def instr() :        #function to repeat instructions 
    print()
    print("""Instructions:
    Use the W,A,S,D keys to move. You can only move one space at a time.
    Press w to move up. Press s to move down. Press a to move left. Press d to move right.
    Press e to exit game.
    Make your way through the maze. Try not to run into ghosts. """)

def exitez(L) :          #function upon exiting
    print("Are you sure you want to leave the game?")
    sure = input("Y/N")
    if sure.lower() == "y" :
        return 1  
    elif sure.lower() == "n" :
        print("Okay! Feel free to explore!")

# def spider(pos_i,pos_j,L) :                    #SUB-GAMES FOR SPIDERS
#     s1,s2,s3,s4,s5 = spider_clusters()         #to identify spider cluster
#     for i in (s1,s2,s3,s4,s5) :
#         for j in i:
#             if (pos_i,pos_j) == j :
#                 cluster = i
#                 break
#             elif (pos_i,pos_j) == (100,100) :
#                 cluster = s1
#                 break
#             elif (pos_i,pos_j) == (200,200) :
#                 cluster = s5
#                 break
#     print()
#     print("The spider has captured you! Play the spider's game to escape!")
#     print()
#
#     if cluster in (s1,s3) :
#         tictactoe(cluster,L)
#     elif cluster in (s2,s4,s5) :
#         sliding(cluster,L)

def win_game(cluster,L) :
    for i in cluster:
        L[i[0]][i[1]] = 0

def lose_game(score):
    print("You bump into the ghosts!!")
    print("Oops, Game Over!")
    print("You get", score, "scores")


def exit_game(cluster,L) :
    for i in cluster:
        L[i[0]][i[1]] = "X"
        
def maze(L,pos_i,pos_j) :       #function to show maze
    if (pos_i-15) < 0 :
        a = 0
    else :
        a = pos_i-15
    if pos_i+15 > len(L)-1 :
        b = len(L)
    else :
        b = pos_i+15
    for i in range(a,b):    
        if pos_j-20 < 0 :
            c = 0
        else :
            c = pos_j-20
        if pos_j+20 > len(L[i])-1 :
            d = len(L[i])
        else :
            d = pos_j+20
        for j in range(c,d):            
            if i==pos_i and j==pos_j:
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

#CODE FOR MOVEMENTS
def play(L,pos_i,pos_j,move, score) :

    while True :
        if L[pos_i][pos_j] != 3 :
            L[pos_i][pos_j] = " "
        
        if move.lower() == "w" :
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
        
        elif move.lower() == "s" :
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
                
        elif move.lower() == "a" :
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

        elif move.lower() == "d" :
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
        
        # elif move == "shortcut1" :
            # spider(100,100,L)
        # elif move == "shortcut2" :
            # spider(200,200,L)
        
        elif move.lower() == "e" :
            r = exitez(L)
            if r == 1 :
                print("Bye!")
                break
        
        if L[pos_i][pos_j] == "E" :
            maze(L,pos_i,pos_j)
            print()
            print("You Win!")
            print("You get total", score, "scores")
            break

        for ghost in ghosts:
            bestAction = randomGhostAction(L,ghost)
            ghost.move(bestAction, L)
            if ghost.row == pos_i and ghost.col == pos_j:
                print("Oops, the ghost catches you!")
                print("you get", score, "scores")

        maze(L,pos_i,pos_j)
        print("You get", score, "scores")
        print("")
        move = input("Enter an action ('w'=up, 's'=down, 'a'=left, 'd'=right, 'e'=exit):")
        print()

#INTRODUCTION AND INITIALISATION
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
            pos_i, pos_j = 14, 17
            break

        else :
            print("Oops! Did you want to say something else?")
    instr()
    maze(L,pos_i,pos_j)
    print()
    move = input("Enter an action ('w'=up, 's'=down, 'a'=left, 'd'=right, 'e'=exit):")
    play(L,pos_i,pos_j,move, score)
