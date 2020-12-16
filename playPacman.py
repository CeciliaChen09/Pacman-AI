""" Game API for Pacman """

import random
from collections import defaultdict
from abc import ABC, abstractmethod
import math
import mcts
import copy
import torch as tr
import pacman_net as pn
import pacman_data as pd
import numpy as np

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
        return self.score == MazeGameBoard.scores_to_win

    def one_step_more(self):
        self.current_steps += 1

class ghost:
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
    initPos = [[2,3],[6,13]] #
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

def smallMaze(ghost_num, slippery_num) :

    L= [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2],
        [2,0,0,0,1,1,0,1,0,0,1,0,1,1,0,2,0,2],
        [2,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,2],
        [2,0,0,0,1,1,0,1,0,0,1,0,1,1,0,2,0,2],
        [2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2],
        [2,0,1,1,0,2,0,1,1,1,1,0,2,0,1,1,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]


    ghosts = []
    ghost.currentIndex = 0

    for i in range(ghost_num):
        ghosts.append(ghost(L))

    count = 0
    while count < slippery_num:
        m = random.randint(1,len(L)-1)
        n = random.randint(1,len(L[0])-1)
        if L[m][n] == 0:
            L[m][n] = 3
            count += 1

    return L, ghosts

def bigMaze(ghost_num, slippery_num):

    L= [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,0,2,0,2,0,2,0,2,1,1,1,2,0,0,0,2,0,0,0,2],
        [2,0,0,0,0,2,0,2,0,0,0,2,0,0,0,0,0,2,0,2,0,2],
        [2,0,0,0,0,2,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,2,0,2],
        [2,0,0,2,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2],
        [2,0,0,2,0,2,1,2,0,2,0,0,0,2,0,2,0,2,0,2,0,2],
        [2,0,0,0,0,2,0,2,0,0,0,0,0,2,0,2,0,0,0,2,0,2],
        [2,0,1,2,0,2,0,2,0,1,0,0,0,0,0,1,0,2,0,2,0,2],
        [2,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,2,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]]



    ghosts = []
    ghost.currentIndex = 0
    for i in range(ghost_num):
        ghosts.append(ghost(L))

    count = 0
    while count < slippery_num:
        m = random.randint(1,len(L)-1)
        n = random.randint(1,len(L[0])-1)
        if L[m][n] == 0:
            L[m][n] = 3
            count += 1

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

def instruction():
    print()
    print("""Instructions:
    The AI Pacman will take his way to move up, down, left or right to eat more dots and avoid being caught by ghosts.
    Wish him good luck!""")
    print()

#function when bumping into a wall
def wall():
    print()
    print("Oops! Ran into a wall! Try again!")
    print()

def win_game(score):
    print()
    print("Good! AI got enough scores and Won!")
    print("Total scores:", score)

def lose_game(score):
    print()
    print("Sorry! AI got caught by ghost and Lost!")
    print("Total scores:", score)

#function to show the maze
def maze(L, pos_i, pos_j):
    for i in range(0, len(L)):
        for j in range(0, len(L[0])):
            if i == pos_i and j == pos_j:
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

def pacmanMove(action, pos_i, pos_j, score, L):
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
    isGameover = False
    nextI = pos_i + directionsDic[action][0]
    nextJ = pos_j + directionsDic[action][1]

    if not isValid(L, nextI, nextJ):
        wall()
    elif L[nextI][nextJ] == "X":
        isGameover = True
    elif L[nextI][nextJ] == 3:
        n = random.randint(0, 4)    #25% chance that the action failed
        if n == 0:
            #print("Oops! Slipped and try again")
            return isGameover, pos_i, pos_j, score

    elif L[nextI][nextJ] == 0:
        score += 10
    # print(L[pos_i][pos_j])
    L[pos_i][pos_j] = " "
    # L[nextI][nextJ] = "#"

    return isGameover, nextI, nextJ, score

def ghostMove(ghosts):
    for ghost in ghosts:
        if ghosts.index(ghost) % 3 == 0:
            bestAction = eclideanGhostAction(L, ghost, pos_i, pos_j)
            ghost.move(bestAction, L)
        elif ghosts.index(ghost) % 3 == 1:
            bestAction = manhanttanGhostAction(L, ghost, pos_i, pos_j)
            ghost.move(bestAction, L)
        elif ghosts.index(ghost) % 3 == 2:
            bestAction = randomGhostAction(L, ghost)
            ghost.move(bestAction, L)

# human player plays the game
def humanPlay(L, pos_i, pos_j):
    score = 0
    while True:
        if L[pos_i][pos_j] == 0:
            L[pos_i][pos_j] = " "
        if L[pos_i][pos_j] == 3:
            L[pos_i][pos_j] = "*"
        
        move = input("Enter an action: ('w'=up, 's'=down, 'a'=left, 'd'=right, 'e'=exit)")
        if move.lower() == "e":
            print("Are you sure you want to leave the game?")
            sure = input("Y/N")
            if sure.lower() == "y":
                print("Bye!")
                break
            else:
                continue
        if move.lower() == "s": action = 0
        if move.lower() == "d": action = 1
        if move.lower() == "w": action = 2
        if move.lower() == "a": action = 3
        isGameover, pos_i, pos_j, score = pacmanMove(action, pos_i, pos_j, score, L)
        ghostMove(ghosts)

        if score >= MazeGameBoard.scores_to_win:
            maze(L, pos_i, pos_j)
            win_game(score)
            break
        isOver = False
        for ghost in ghosts:
            if ghost.row == pos_i and ghost.col == pos_j:
                maze(L, pos_i, pos_j)
                lose_game(score)
                isOver = True
                break
        if isOver: break
        
        maze(L, pos_i, pos_j)
        print("Scores:", score)
        print()

# baseline AI which chooses actions uniformly at random
def randomAI(L, pos_i, pos_j):
    score = 0
    while True:
        if L[pos_i][pos_j] == 0:
            L[pos_i][pos_j] = " "
        if L[pos_i][pos_j] == 3:
            L[pos_i][pos_j] = "*"

        directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]
        action = random.randint(0, 3)
        nextI = pos_i + directionsDic[action][0]
        nextJ = pos_j + directionsDic[action][1]
        while not isValid(L, nextI, nextJ):
            action = random.randint(0, 3)
            nextI = pos_i + directionsDic[action][0]
            nextJ = pos_j + directionsDic[action][1]
        
        if action == 0: nextaction = "down"
        elif action == 1: nextaction = "right"
        elif action == 2: nextaction = "up"
        elif action == 3: nextaction = "left"
        print("AI's next action:", nextaction)
        input("Press Enter to continue...")
        isGameover, pos_i, pos_j, score = pacmanMove(action, pos_i, pos_j, score, L)
        ghostMove(ghosts)

        if score >= MazeGameBoard.scores_to_win:
            maze(L, pos_i, pos_j)
            win_game(score)
            break

        isOver = False
        for ghost in ghosts:
            if ghost.row == pos_i and ghost.col == pos_j:
                maze(L, pos_i, pos_j)
                lose_game(score)
                isOver = True
                break
        if isOver: break
        
        maze(L, pos_i, pos_j)
        print("Scores:", score)
        print()

def retriveInfoFromGameBoard(gameBoard):
    return gameBoard.board, gameBoard.pac_i, gameBoard.pac_j, gameBoard.score

# MCTS AI play the game
def mctsAI(gameBoard, tree, enableHandEnter):
    boardStateNode = mcts.pacmanNode(gameBoard, 0)
    totalNodeCount = 0
    while True:
        nodesCount = 0
        L0, pos_i0, pos_j0, score0 = retriveInfoFromGameBoard(boardStateNode.board)
        for i in range(50):
            nodesCount += tree.do_rollout(boardStateNode)
        if enableHandEnter:
            print("Current Turns:", boardStateNode.board.current_steps)
        boardStateNode.board.one_step_more()
        if boardStateNode.is_terminal():
            break
        boardStateNode, boardStateScoreForNN = tree.choose(boardStateNode)
        L, pos_i, pos_j, score = retriveInfoFromGameBoard(boardStateNode.board)
        
        if (pos_i - pos_i0) == 1: nextaction = "down"
        elif (pos_j - pos_j0) == 1: nextaction = "right"
        elif (pos_i0 - pos_i) == 1: nextaction = "up"
        elif (pos_j0 - pos_j) == 1: nextaction = "left"
        
        if enableHandEnter:
            print("AI's next action:", nextaction)
            input("Press Enter to continue...")

        if L[pos_i][pos_j] != 3:
            L[pos_i][pos_j] = " "
        
        if boardStateNode.is_terminal() == True:
            break
        
        ghosts = boardStateNode.board.ghosts
        for ghost in ghosts:
            if(ghosts.index(ghost) % 3 == 0):
                bestAction = eclideanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)
            elif(ghosts.index(ghost) % 3 == 1):
                bestAction = manhanttanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)
            elif (ghosts.index(ghost) % 3 == 2):
                bestAction = randomGhostAction(L, ghost)
                ghost.move(bestAction, L)
        
        if enableHandEnter:
            maze(L, pos_i, pos_j)
            print("The number of tree nodes processed:", nodesCount)
            print("Scores:", score)
            print()
        totalNodeCount += nodesCount

        # set the depth to 0 for the next round of AI search
        boardStateNode = mcts.pacmanNode(boardStateNode.board, 0)
    
    if boardStateNode.board.isWon():
        if enableHandEnter:
            maze(L, pos_i, pos_j)
            win_game(score)
        return totalNodeCount, score, True
    elif boardStateNode.board.isCaught():
        if enableHandEnter:
            maze(L, pos_i, pos_j)
            lose_game(score)
        return totalNodeCount, score, False
    else:
        if enableHandEnter:
            maze(L, pos_i, pos_j)
            print("Total scores:", score)
            print("The maximum steps pass, AI tied the game")
        return totalNodeCount, score, False



def nn_puct(node, L, mode):
    net = pn.BlockusNet3(L)
    if mode == "big_1_3":
        net.load_state_dict(tr.load("model_net3_big_1_3.pth" ))
    elif mode == "big_2_3":
        net.load_state_dict(tr.load("model_net3_big_2_3.pth" ))
    elif mode == "big_2_5":
        net.load_state_dict(tr.load("model_net3_big_2_5.pth" ))
    elif mode == "small_1_3":
        net.load_state_dict(tr.load("model_net3_small_1_3.pth" ))
    elif mode == "small_2_5":
        net.load_state_dict(tr.load("model_net3_small_2_5.pth" ))

    with tr.no_grad():
        children = list(node.find_children())
        x = tr.stack(tuple(map(pd.encode, [child for child in children])))
        y = net(x)

        probs = tr.softmax(y.flatten(), dim=0)
        a = np.random.choice(len(probs), p=probs.detach().numpy())
    return list(node.find_children())[a]



def mcts_nnAI(gameBoard, mode, enableHandEnter):
    tree = mcts.MCTS(choose_method = nn_puct, mode = mode)
    boardStateNode = mcts.pacmanNode(gameBoard, 0)
    totalNodeCount = 0
    while True:
        nodesCount = 0
        L0, pos_i0, pos_j0, score0 = retriveInfoFromGameBoard(boardStateNode.board)
        for i in range(15):
            nodesCount += tree.do_rollout(boardStateNode)
        if enableHandEnter:
            print("Current Turns:", boardStateNode.board.current_steps)
        boardStateNode.board.one_step_more()
        if boardStateNode.is_terminal():
            break
        boardStateNode, boardStateScoreForNN = tree.choose(boardStateNode)
        L, pos_i, pos_j, score = retriveInfoFromGameBoard(boardStateNode.board)

        if (pos_i - pos_i0) == 1: nextaction = "down"
        elif (pos_j - pos_j0) == 1: nextaction = "right"
        elif (pos_i0 - pos_i) == 1: nextaction = "up"
        elif (pos_j0 - pos_j) == 1: nextaction = "left"

        if enableHandEnter:
            print("AI's next action:", nextaction)
            input("Press Enter to continue...")

        if L[pos_i][pos_j] != 3:
            L[pos_i][pos_j] = " "

        if boardStateNode.is_terminal() == True:
            break

        ghosts = boardStateNode.board.ghosts
        for ghost in ghosts:
            if(ghosts.index(ghost) % 3 == 0):
                bestAction = eclideanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)
            elif(ghosts.index(ghost) % 3 == 1):
                bestAction = manhanttanGhostAction(L, ghost, pos_i, pos_j)
                ghost.move(bestAction, L)
            elif (ghosts.index(ghost) % 3 == 2):
                bestAction = randomGhostAction(L, ghost)
                ghost.move(bestAction, L)

        if enableHandEnter:
            maze(L, pos_i, pos_j)
            print("The number of tree nodes processed:", nodesCount)
            print("Scores:", score)
            print()
        totalNodeCount += nodesCount

        # set the depth to 0 for the next round of AI search
        boardStateNode = mcts.pacmanNode(boardStateNode.board, 0)

    if boardStateNode.board.isWon():
        if enableHandEnter:
            maze(L, pos_i, pos_j)
            win_game(score)
        return totalNodeCount, score, True
    elif boardStateNode.board.isCaught():
        if enableHandEnter:
            maze(L, pos_i, pos_j)
            lose_game(score)
        return totalNodeCount, score, False
    else:
        if enableHandEnter:
            maze(L, pos_i, pos_j)
            print("Total scores:", score)
            print("The maximum steps pass, AI tied the game")
        return totalNodeCount, score, False




if __name__ == "__main__":
    while True :
        load = input("""Please choose the problem size:
    1) Enter 1 to choose big maze with 1 ghost and 3 slippery positions
    2) Enter 2 to choose small maze with 1 ghost and 3 slippery positions
    3) Enter 3 to choose big maze with 2 ghosts and 3 slippery positions
    4) Enter 4 to choose small maze with 2 ghosts and 5 slippery positions
    5) Enter 5 to choose big maze with 2 ghosts and 5 slippery positions
""")
        score = 0
        if load == "1":
            L, ghosts = bigMaze(1,3)
            pos_i, pos_j = 3, 8
            mode = "big_1_3"
            break
        elif load == "2":
            L, ghosts = smallMaze(1,3)
            pos_i, pos_j = 5, 10
            mode = "small_1_3"
            break
        elif load == "3":
            L, ghosts = bigMaze(2,3)
            pos_i, pos_j = 3, 8
            mode = "big_2_3"
            break
        elif load == "4":
            L, ghosts = smallMaze(2,5)
            pos_i, pos_j = 5, 10
            mode = "small_2_5"
            break
        elif load == "5":
            L, ghosts = bigMaze(2,5)
            pos_i, pos_j = 5, 10
            mode = "big_2_5"
            break
        else:
            print("Please enter 1,2,3,4 or 5")
    
    while True:
        ai_chosen = input("""Please choose the control strategy:
    1) Enter 1 to choose human player
    2) Enter 2 to choose baseline AI
    3) Enter 3 to choose tree-based AI (Enter 5 to run 100 times)
    4) Enter 4 to choose tree+NN-based AI(Enter 6 to run 100 times)
""")
        if ai_chosen == "1" :
            gameMode = "human player"
            break
        elif ai_chosen == "2" :
            gameMode = "baseline AI"
            break
        elif ai_chosen == "3" :
            gameMode = "tree-based AI"
            break
        elif ai_chosen == "4" :
            gameMode = "tree+NN-based AI"
            break
        elif ai_chosen == "5":
            gameMode = "automatic"
            break
        elif ai_chosen == "6":
            gameMode = "automatic tree+NN-based AI"
            break
        else:
            print("Please enter 1,2,3 4, 5, 6")
    
    instruction()
    print("Game mode:", gameMode)
    print()
    maze(L,pos_i,pos_j)
    print()
    
    initBoard = MazeGameBoard(L, ghosts, pos_i, pos_j, 0)

    tree = mcts.MCTS()
    
    if ai_chosen == "1":
        humanPlay(L, pos_i, pos_j)
    
    elif ai_chosen == "2":
        randomAI(L, pos_i, pos_j)
    
    elif ai_chosen == "3":
        totalnodescount, finalscore, aiWon = mctsAI(copy.deepcopy(initBoard), tree, True)
        print("The total number of tree nodes processed in this game is", totalnodescount)

    elif ai_chosen == "4":
        totalnodescount, finalscore, aiWon = mcts_nnAI(copy.deepcopy(initBoard), mode, True)
        print("The total number of tree nodes processed in this game is", totalnodescount)

        
    elif ai_chosen == "5":
        nodes_list = [0]
        scores_list = [0]
        col = ['white']
        for i in range(100):
            totalnodescount = 0
            totalnodescount, finalscore, aiWon = mctsAI(copy.deepcopy(initBoard), tree, False)
            print("Game", i+1, ":", totalnodescount, "  Score:", finalscore)
            nodes_list.append(totalnodescount)
            scores_list.append(finalscore)
            if aiWon: col.append('#87CEFA')
            else: col.append('#FFA500')
        
        import matplotlib.pyplot as plt
        plt.bar(range(len(nodes_list)), nodes_list, width=1.0, color=col)
        plt.xlabel("Games")
        plt.ylabel("Number of tree nodes processed")
        plt.title("Efficiency")
        plt.show()

        plt.bar(range(len(scores_list)), scores_list, width=1.0, color=col)
        plt.xlabel("Games")
        plt.ylabel("Final scores")
        plt.title("Performance")
        plt.show()

    elif ai_chosen == "6":
        nodes_list = [0]
        scores_list = [0]
        col = ['white']
        for i in range(100):
            totalnodescount = 0
            totalnodescount, finalscore, aiWon = mcts_nnAI(copy.deepcopy(initBoard), False)
            # print("Game", i+1, ":", totalnodescount, "  Score:", finalscore)
            nodes_list.append(totalnodescount)
            scores_list.append(finalscore)
            if aiWon: col.append('#87CEFA')
            else: col.append('#FFA500')

        import matplotlib.pyplot as plt
        plt.bar(range(len(nodes_list)), nodes_list, width=1.0, color=col)
        plt.xlabel("Games")
        plt.ylabel("Number of tree nodes processed")
        plt.title("Efficiency")
        plt.show()

        plt.bar(range(len(scores_list)), scores_list, width=1.0, color=col)
        plt.xlabel("Games")
        plt.ylabel("Final scores")
        plt.title("Performance")
        plt.show()

