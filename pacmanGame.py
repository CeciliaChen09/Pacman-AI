""" Game API for Pacman """

import random
from collections import defaultdict
from abc import ABC, abstractmethod
import math
import mcts
import copy

class Node(ABC):
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]

    @abstractmethod
    #find all the successors of the state
    def find_children(self):
        return set()

    @abstractmethod
    def random_child(self):
        return None

    # return true if no child
    @abstractmethod
    def is_leaf(self):
        return True

    #score
    @abstractmethod
    def score(self):
        return 0

    @abstractmethod
    #node must be hashable
    def __hash__(self):
        return 123456

    @abstractmethod
    #nodes should be comparable
    def __eq__(node1, node2):
        return True

class MazeGameBoard():
    scores_to_win = 100
    max_steps = 40
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
    def __init__(self, L, ghosts, pos_i, pos_j, score):
        self.board = L
        self.ghosts = ghosts
        self.pac_i = pos_i
        self.pac_j = pos_j
        self.score = score
        self.current_steps = 0
        # 0 for pacman 1 for ghost turn

    def gameOver(self):
        return self.isCaught() or self.isWon() or self.current_steps >= MazeGameBoard.max_steps
    def isCaught(self):
        for ghost in self.ghosts:
            if self.pac_i == ghost.row and self.pac_j == ghost.col:
                return True
        return False

    def isWon(self):
        return self.score >= MazeGameBoard.scores_to_win

    def one_step_more(self):
        self.current_steps += 1

class ghost:

    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
    initPos = [[2,3],[6,13],[8,7],[1,16]] #
    currentIndex = 0
    oldpoint = 0

    def __init__(self, L):
        # 0: i++(go down), 1: j++ (go right), 2:i--(go up), 3: j-- (go left)
        self.dir = random.randint(0,3)
        if self.currentIndex >= len(self.initPos):
            raise RuntimeError("try to init too many ghosts")

        m = self.initPos[self.currentIndex][0]
        n = self.initPos[self.currentIndex][1]
        L[m][n] = 'X'
        self.row = m
        self.col = n
        ghost.currentIndex += 1

    def move(self, go, L):
        if self.oldpoint == 'X' :
            L[self.row][self.col] = 0
        else :
            L[self.row][self.col] = self.oldpoint
        self.row += self.directionsDic[go][0]
        self.col += self.directionsDic[go][1]
        self.oldpoint = L[self.row][self.col]
        L[self.row][self.col] = 'X'

def smallMaze(num) :

    L= [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2],
        [2,0,2,0,1,1,0,1,0,0,1,0,1,1,0,2,0,2],
        [2,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,2],
        [2,0,2,0,1,1,0,1,0,0,1,0,1,1,0,2,0,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2],
        [2,0,1,1,0,2,0,1,1,1,1,0,2,0,1,1,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]

    ghosts = []
    for i in range(num):         #randomly generated ghosts
        ghosts.append(ghost(L))

    count = 0
    while count < 5:             #randomly generated slippery positions
        m = random.randint(1,len(L)-1)
        n = random.randint(1,len(L[0])-1)
        if L[m][n] == 0:
            L[m][n] = 3
            count += 1

    return L, ghosts

def bigMaze(num):

    L= [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,0,2,0,2,0,2,0,2,1,1,1,2,0,2,1,2,0,2,0,2],
        [2,0,0,2,0,2,0,2,0,0,0,2,0,0,0,0,0,2,0,2,0,2],
        [2,0,0,2,0,2,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0,2],
        [2,0,1,2,0,0,0,0,0,0,0,2,0,2,0,1,1,2,0,2,0,2],
        [2,0,0,2,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2],
        [2,0,0,2,0,2,1,2,0,2,0,0,0,2,0,2,0,2,0,2,0,2],
        [2,0,0,0,0,2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,2],
        [2,0,1,2,0,2,0,2,0,1,1,0,1,2,1,1,0,2,0,2,0,2],
        [2,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]

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

# the ghost changes his direction
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

def eclideanGhostAction(L, ghost, pos_i, pos_j):
    i = ghost.row
    j = ghost.col
    dir = [[1,0], [0,1], [-1,0], [0,-1]]

    distance = []
    for n in range(4):
        a = i + dir[n][0]
        b = j + dir[n][1]
        if isValid(L, a, b):
            dis = ((pos_i - a)**2 + (pos_j - b)**2)**(1/2)
            distance.append(dis)
        else:
            distance.append(float("inf"))
    minDis = min(distance)
    return distance.index(minDis)

def manhanttanGhostAction(L, ghost, pos_i, pos_j):
    i = ghost.row
    j = ghost.col
    dir = [[1,0], [0,1], [-1,0], [0,-1]]
    distance = []
    for n in range(4):
        a = i + dir[n][0]
        b = j + dir[n][1]
        if isValid(L, a, b):
            dis = abs(pos_i - a) + abs(pos_j - b)
            distance.append(dis)
        else:
            distance.append(float("inf"))
    minDis = min(distance)
    return distance.index(minDis)

def isValid(L, i, j):
    if i<= 0 or j<=0 or i >= len(L) - 1 or j>= len(L[0]) - 1 or L[i][j] == 1 or L[i][j] == 2:
        return False
    return True

def instruction() :
    print()
    print("""Instructions:
    The AI Pacman will take his way to move up, down, left or right
to eat more dots and avoid being caught by ghosts.
    Wish him good luck!""")
    print()

#function when bumping into a wall
def wall() :
    print()
    print("Oops! Ran into a wall! Try again!")
    print()

#function when going into slippery position
def slippery() :
    n = random.randint(0, 4)
    #25% chance that the action failed
    if n == 0 :
        return True
    else :
        return False

#function to exit the game
def exit_game(L) :
    print("Are you sure you want to leave the game?")
    sure = input("Y/N ")
    if sure.lower() == "y" :
        #print("Oops! You slipped! Try again!")
        return 1
    elif sure.lower() == "n" :
        print("Okay! Feel free to explore!")

def win_game(score) :
    print()
    print("Good! AI got enough scores and Won!")
    print("Total scores:", score)

def lose_game(score):
    print()
    print("Sorry! AI got caught by ghost and Lost!")
    print("Total scores:", score)

#function to show the maze
def maze(L, pos_i, pos_j) :
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

#baseline AI which chooses actions uniformly at random
def randomAI(L, pos_i, pos_j):
    score = 0
    while True:
        if L[pos_i][pos_j] == 0 :  #eat the dot
            L[pos_i][pos_j] = " "
        
        directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
        action = random.randint(0, 3)
        nextI = pos_i + directionsDic[action][0]
        nextJ = pos_j + directionsDic[action][1]
        while not isValid(L, nextI, nextJ):
            action = random.randint(0, 3)
            nextI = pos_i + directionsDic[action][0]
            nextJ = pos_j + directionsDic[action][1]
        
        if action == 0:
            print("AI's next action: down")
        elif action == 1:
            print("AI's next action: right")
        elif action == 2:
            print("AI's next action: up")
        elif action == 3:
            print("AI's next action: left")
        
        input("Press Enter to continue...")
        isGameover, pos_i, pos_j, score = pacmanMove(action, pos_i, pos_j, score, L)
        
        if score >= 100:
            maze(L, pos_i, pos_j)
            win_game(score)
            break
        
        isOver = False
        for ghost in ghosts:
            if ghosts.index(ghost) % 3 == 1 :
                bestAction = randomGhostAction(L, ghost)
                ghost.move(bestAction, L)
                if ghost.row == pos_i and ghost.col == pos_j:
                    maze(L, pos_i, pos_j)
                    lose_game(score)
                    isOver = True
                    break
            elif ghosts.index(ghost) % 3 == 0 :
                bestAction = eclideanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)
                if ghost.row == pos_i and ghost.col == pos_j:
                    maze(L, pos_i, pos_j)
                    lose_game(score)
                    isOver = True
                    break
            elif ghosts.index(ghost) % 3 == 2 :
                bestAction = manhanttanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)
                if ghost.row == pos_i and ghost.col == pos_j:
                    maze(L, pos_i, pos_j)
                    lose_game(score)
                    isOver = True
                    break
        if isOver :
            break
        
        maze(L,pos_i,pos_j)
        print("Scores:", score)
        print()
    
    return score

def pacmanMove(action, pos_i, pos_j, score, L):
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
    isGameover = False
    
    if(L[pos_i][pos_j] == 3 and slippery()):
        return isGameover, pos_i, pos_j, score
    nextI = pos_i + directionsDic[action][0]
    nextJ = pos_j + directionsDic[action][1]
    if not isValid(L, nextI, nextJ):
        wall()
    elif L[nextI][nextJ] == "X":
        #lose_game(score)
        isGameover = True
    elif L[nextI][nextJ] == 0:
        pos_i = pos_i + directionsDic[action][0]
        pos_j = pos_j + directionsDic[action][1]
        score += 10
    elif L[nextI][nextJ] == " ":
        pos_i = pos_i + directionsDic[action][0]
        pos_j = pos_j + directionsDic[action][1]

    return isGameover, pos_i, pos_j, score

def retriveInfoFromGameBoard(gameBoard):
    return gameBoard.board, gameBoard.pac_i, gameBoard.pac_j, gameBoard.score

def play(gameBoard, tree, enableHandEnter):      # MCTS AI play the game 
    boardStateNode = mcts.pacmanNode(gameBoard, 0)
    totalcounts = 0
    while True:
        L0, pos_i0, pos_j0, score0 = retriveInfoFromGameBoard(boardStateNode.board)
        for i in range(50):
            tree.do_rollout(boardStateNode)
        
        print("Current Turns:", boardStateNode.board.current_steps)
        boardStateNode.board.one_step_more()
        if boardStateNode.is_terminal():
            break
        boardStateNode = tree.choose(boardStateNode)
        L, pos_i, pos_j, score = retriveInfoFromGameBoard(boardStateNode.board)
        
        if (pos_i - pos_i0) == 1:
            nextaction = "down"
        elif (pos_i0 - pos_i) == 1:
            nextaction = "up"
        elif (pos_j - pos_j0) == 1:
            nextaction = "right"
        elif (pos_j0 - pos_j) == 1:
            nextaction = "left"
        
        if enableHandEnter:
            print("AI's next action:", nextaction)
            input("Press Enter to continue...")
        
        if L[pos_i][pos_j] != 3 :       #eat the dot
            L[pos_i][pos_j] = " "
        
        #pacman's turn
        if boardStateNode.is_terminal() == True:
            break
        # the ghosts' turn
        ghosts = boardStateNode.board.ghosts
        for ghost in ghosts:
            if ghosts.index(ghost) % 3 == 2:
                bestAction = randomGhostAction(L,ghost)
                ghost.move(bestAction, L)

            elif(ghosts.index(ghost) % 3 == 0):
                bestAction = eclideanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)

            elif(ghosts.index(ghost) % 3 == 1):
                bestAction = manhanttanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)
        
        # set the depth to 0 for the next round of ai search
        boardStateNode = mcts.pacmanNode(boardStateNode.board, 0)
        
        maze(L,pos_i,pos_j)
        print("The number of tree nodes processed:", tree.count)
        print("Scores:", score)
        print()
        totalcounts += tree.count
    
    if boardStateNode.board.isWon():
        maze(L,pos_i,pos_j)
        print("The number of tree nodes processed:", tree.count)
        win_game(score)
        return totalcounts
    elif boardStateNode.board.isCaught():
        maze(L,pos_i,pos_j)
        print("The number of tree nodes processed:", tree.count)
        lose_game(score)
        return totalcounts
    else:
        print("The number of tree nodes processed:", tree.count)
        print("Total scores:", score)
        print("maxium steps pass, AI Tie the game")
        return totalcounts

if __name__ == "__main__":
    while True:
        ai_chosen = input("""Which AI will you choose?
    1) Press 1 to choose random AI
    2) Press 2 to choose tree-based AI
""")
        if ai_chosen == "1" :
            gameMode = "random AI"
            break
        elif ai_chosen == "2" :
            gameMode = "MCTS AI"
            break
        else:
            print("Please input 1 or 2")
    
    while True :
        load = input("""Which maze do you want?
    1) Press 1 to choose small maze
    2) Press 2 to choose big maze
""")
        score = 0
        if load == "1" :
            L, ghosts = smallMaze(2)
            pos_i, pos_j = 3, 8
            break
        elif load == "2" :
            L, ghosts = bigMaze(2)
            pos_i, pos_j = 7, 11
            break
        else :
            print("Please input 1 or 2")
    
    instruction()
    print("Game mode: ", gameMode)
    print()
    maze(L,pos_i,pos_j)
    print()
    
    initBoard = MazeGameBoard(L, ghosts, pos_i, pos_j, 0)
    tree = mcts.MCTS()
    
    if ai_chosen == "1":
        randomAI(L, pos_i, pos_j)
    
    elif ai_chosen == "2":
        totalnodescount = play(copy.deepcopy(initBoard), tree, True)
        print("The total number of tree nodes processed in this game is", totalnodescount)
