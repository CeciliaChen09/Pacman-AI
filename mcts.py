""" Monte-carlo tree search """

from collections import defaultdict
from abc import ABC, abstractmethod
import pacmanGame as pac
import math
import random
import copy

class Node(ABC):
    directionsDic = [[1,0], [0,1], [-1,0], [0,-1]]

    @abstractmethod
    #find all the successors of the state
    def find_children(self):
        return set()

    @abstractmethod
    def find_random_child(self):
        return None

    # return true if no child
    @abstractmethod
    def is_terminal(self):
        return True

    #score
    @abstractmethod
    def reward(self):
        return 0

    @abstractmethod
    #node must be hashable
    def __hash__(self):
        return 123456

    @abstractmethod
    #nodes should be comparable
    def __eq__(node1, node2):
        return True

class pacmanNode(Node):
    # 0 turn for pacman turn, 1 turn for ghost turn
    maxDepth = 40
    def __init__(self, board, currentDepth):
        self.board = board
        self.turn = 0
        self.depth = currentDepth

    def find_children(self):
        board = self.board
        children = set()
        # find all next possible move here
        for i in range(4):
            next_i = board.pac_i + board.directionsDic[i][0]
            next_j = board.pac_j + board.directionsDic[i][1]
            if not pac.isValid(board.board, next_i, next_j):
                continue
            newboard = board.board.copy()
            _,_,_, newscore = pac.pacmanMove(i, board.pac_i, board.pac_j, board.score, newboard)
            children.add(GhostNode(pac.MazeGameBoard(newboard, board.ghosts, next_i, next_j, newscore), self.depth+1))
        return children

    def find_random_child(self):
        board = self.board
        randomList = [0,1,2,3]
        random.shuffle(randomList)
        index = 0
        # find a random vaild child
        while True:
            i = randomList[index]
            next_i = board.pac_i + board.directionsDic[i][0]
            next_j = board.pac_j + board.directionsDic[i][1]
            if pac.isValid(board.board, next_i, next_j):
                newboard = board.board.copy()
                _,_,_, newscore = pac.pacmanMove(i, board.pac_i, board.pac_j, board.score, newboard)
                return GhostNode(pac.MazeGameBoard(newboard, board.ghosts, next_i, next_j, newscore), self.depth+1)
            index += 1

    def is_terminal(self):
        return self.board.gameOver() or self.depth >= pacmanNode.maxDepth

    def reward(self):
        if not self.is_terminal():
            raise RuntimeError(f"reward called on nonterminal board {self.board}")
        if self.board.isWon():
            return 1
        if self.board.isCaught():
            return 0.1
        else:
            return 0.5
    #node must be hashable
    def __hash__(self):
        feature =  (self.board.pac_i, self.board.pac_j, self.board.ghosts[0].row, self.board.ghosts[0].col, self.board.ghosts[1].row, self.board.ghosts[1].col,self.turn)
        return hash(feature)

    #nodes should be comparable
    def __eq__(node1, node2):
        return node1.board.board == node2.board.board and node1.turn == node2.turn

class GhostNode(Node):
    maxDepth = 40
    def __init__(self,board, currentDepth):
        self.board = board
        self.turn = 1
        self.depth  = currentDepth

    def find_children(self):
        # assume we only have 2 ghosts, write it tight, very stupid approach
        ghost1 = self.board.ghosts[0]
        ghost2 = self.board.ghosts[1]
        children = set()
        for i in range(4):
            next_i_g1 = ghost1.row + self.board.directionsDic[i][0]
            next_j_g1 = ghost1.col + self.board.directionsDic[i][1]
            if not pac.isValid(self.board.board, next_i_g1, next_j_g1):
                continue
            for j in range(4):
                next_i_g2 = ghost2.row + self.board.directionsDic[j][0]
                next_j_g2 = ghost2.col + self.board.directionsDic[j][1]
                if not pac.isValid(self.board.board, next_i_g2, next_j_g2):
                    continue
                newboard = copy.deepcopy(self.board.board)
                newghost1= copy.deepcopy(ghost1)
                newghost2 = copy.deepcopy(ghost2)
                newghost1.move(i, newboard)
                newghost2.move(j, newboard)
                newghosts =[newghost1, newghost2]
                newMazeGameBoard = pac.MazeGameBoard(newboard,newghosts, self.board.pac_i, self.board.pac_j, self.board.score)
                children.add(pacmanNode(newMazeGameBoard,self.depth))
        return children

    def find_random_child(self):
        board = self.board
        ghost0 = self.board.ghosts[0]
        ghost1 = self.board.ghosts[1]
        # find a random vaild child
        while True:
            i = random.randint(0,3)
            next_i_g0 = ghost0.row + board.directionsDic[i][0]
            next_j_g0 = ghost0.col + board.directionsDic[i][1]
            if pac.isValid(board.board, next_i_g0, next_j_g0):
                while True:
                    j = random.randint(0,3)
                    next_i_g1 = ghost1.row + board.directionsDic[j][0]
                    next_j_g1 = ghost1.col + board.directionsDic[j][1]
                    if pac.isValid(board.board, next_i_g1, next_j_g1):
                        newboard = copy.deepcopy(board.board)
                        newghost0= copy.deepcopy(ghost0)
                        newghost1 = copy.deepcopy(ghost1)
                        newghost0.move(i, newboard)
                        newghost1.move(j, newboard)
                        newghosts =[newghost0, newghost1]
                        newMazeGameBoard = pac.MazeGameBoard(newboard,newghosts, board.pac_i, board.pac_j,board.score)
                        return pacmanNode(newMazeGameBoard, self.depth)

    def is_terminal(self):
        return self.board.gameOver() or self.depth>= GhostNode.maxDepth

    def reward(self):
        if not self.is_terminal():
            raise RuntimeError(f"reward called on nonterminal board {self.board}")
        if self.board.isWon():
            #print("reward 1")
            return 0
        if self.board.isCaught():
            #print("reward 0")
            return 1
        else:
            #print("reward 0.5")
            return 0.5
    #node must be hashable
    def __hash__(self):
        feature =  (self.board.pac_i, self.board.pac_j, self.board.ghosts[0].row, self.board.ghosts[0].col, self.board.ghosts[1].row, self.board.ghosts[1].col,self.turn)
        return hash(feature)
    def __eq__(node1, node2):
        return node1.board.board == node2.board.board and node1.turn == node2.turn

class MCTS:
    nodeVisitedEachTurn = 0
    count = 0
    def __init__(self, exploration_weight = 1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        current_steps = node.board.current_steps
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        nextNode = max(self.children[node], key=score)
        nextNode.board.current_steps = current_steps
        return nextNode

    def do_rollout(self, node):
        MCTS.nodeVisitedEachTurn = 0
        path = self._select(node)
        MCTS.nodeVisitedEachTurn += len(path)
        leaf = path[-1]
        self._expand(leaf)
        #print("after expand")
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)
        MCTS.count += MCTS.nodeVisitedEachTurn

    def _select(self, node):
        path = []
        #print("start")
        while True:
            #print(node.is_terminal())
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            for n in self.children[node]:
                if not n in self.children:
                    path.append(n)
                    return path
            node = self._uct_select(node, path)  # descend a layer deeper
        #print("end")

    def _expand(self, node):
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _simulate(self, node):
        MCTS.nodeVisitedEachTurn += 1
        invert_reward = True
        while True:
            #print(node.depth)
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            node = node.find_random_child()
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1- reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node, path):
        # All children of node should already be expanded:
        for n in self.children[node]:
            if not n in self.children:
                # print(" n problem!", n )
                unexplored = self.children[node] - self.children.keys()
                # print("unexplore list(should not be empty :", unexplored)
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )
        
        sortedList = sorted(self.children[node], key = uct)
        i = -1
        #print(sortedList[-1] == node)
        while(sortedList[i] in path):
            # print(" not good, loop in tree")
            i -= 1
        return sortedList[i]
    
