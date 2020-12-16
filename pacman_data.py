import itertools as it
import mcts as mcts
import playPacman as pp
import numpy as np
import torch as tr



def generate_small_maze25(num_games=25, num_rollout= 50):

    # board_state_node = mcts.pacmanNode(game_board, 0)
    data = []

    for game in range(num_games):
        # initialization for the next round of AI search
        L, ghosts = pp.smallMaze(2,5)
        pos_i, pos_j = 5, 10
        init_board = pp.MazeGameBoard(L, ghosts, pos_i, pos_j, 0)
        tree = mcts.MCTS()
        board_state_node = mcts.pacmanNode(init_board, 0)

        while True:
            L0, pos_i0, pos_j0, score0 = pp.retriveInfoFromGameBoard(board_state_node.board)

            for num in range(num_rollout):
                tree.do_rollout(board_state_node)
            board_state_node.board.one_step_more()

            # print(board_state_node.board.current_steps)
            board_state_node, max_score = tree.choose(board_state_node)

            if board_state_node.is_terminal():
                data = get_data(tree, data)
                break

            maze, pos_i, pos_j, score = pp.retriveInfoFromGameBoard(board_state_node.board)

            if maze[pos_i][pos_j]!= 3:
               maze[pos_i][pos_j] = " "

            if board_state_node.is_terminal():
                data = get_data(tree, data)
                break

            ghosts = board_state_node.board.ghosts
            for ghost in ghosts:
                if(ghosts.index(ghost) % 3 == 0):
                    bestAction = pp.eclideanGhostAction(maze, ghost, pos_i, pos_j)
                    ghost.move(bestAction, maze)
                elif(ghosts.index(ghost) % 3 == 1):
                    bestAction = pp.manhanttanGhostAction(maze, ghost, pos_i, pos_j)
                    ghost.move(bestAction, maze)
                elif (ghosts.index(ghost) % 3 == 2):
                    bestAction = pp.randomGhostAction(maze, ghost)
                    ghost.move(bestAction, maze)

            if board_state_node.is_terminal():
                data = get_data(tree, data)
                break

        # for child in max_node.children():
        #     data.append((child, mcts.get_score_estimates(child)))

    return data

def get_data(tree, data):

    for node in list(tree.N):
        if type(node) is mcts.pacmanNode:
            continue
        data.append((node, tree.get_score_estimates(node)))
    return data



def encode(state):
    board_state = state.board.board
    length = len(board_state)
    width = len(board_state[0])
    # board = np.zeros((length, width))
    board = [[0 for x in range(width)] for y in range(length)]

    for i in range (len(board)):
        for j in range (len(board[0])):
            if board_state[i][j] == 0:
                board[i][j] = 0
            elif board_state[i][j] == 1:
                board[i][j] = 1
            elif board_state[i][j] == 2:
                board[i][j] = 2
            elif board_state[i][j] == "*" or board_state[i][j] == 3:
                board[i][j] = 3
            elif board_state[i][j] == "X":
                board[i][j] = 4
            elif board_state[i][j] == "#":
                board[i][j] = 5
            elif board_state[i][j] == " ":
                board[i][j] = 6


    label = tr.as_tensor(board)
    index = tr.reshape(label, (1, len(label) * len(label[0])))
    # print(index.size())
    output = tr.zeros(7, len(label) * len(label[0])).scatter(0, index, 1)
    # print(index.size())

    one_hot = tr.reshape(output, (7, len(label), len(label[0])))

    return one_hot


def get_batch():
    training_data= generate_small_maze25(num_games=25, num_rollout= 50)
    states = []
    scores = []
    for data in training_data: # state_score_pair
        states.append(encode(data[0]))
        scores.append(tr.tensor(data[1]))

    inputs = tr.stack(states, dim = 0)
    scores = tr.FloatTensor(scores)
    outputs = tr.reshape(scores, (len(scores), 1))


    return inputs, outputs


if __name__ == "__main__":


    inputs, outputs = get_batch()


    import pickle as pk
    with open("data_small_2_5.pkl" , "wb") as f: pk.dump((inputs, outputs), f)





























