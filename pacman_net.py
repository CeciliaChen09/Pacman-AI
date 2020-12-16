
import numpy as np
import torch as tr
import playPacman as pp

def BlockusNet1(board):
    module =  tr.nn.Sequential(
        tr.nn.Flatten(),
        tr.nn.Linear(7 * len(board) * len(board[0]), 1)
    )
    return module


def BlockusNet3(board):
    module = tr.nn.Sequential(
        tr.nn.Flatten(),
        tr.nn.Linear(7 * len(board) * len(board[0]), 256),
        tr.nn.ReLU(),
        tr.nn.Linear(256, 64),
        tr.nn.ReLU(),
        tr.nn.Linear(64, 1)

    )
    return module

def BlockusNet2(board):
    module =  tr.nn.Sequential(
        tr.nn.Flatten(),
        tr.nn.Linear(7 * len(board) * len(board[0]), 1),
        tr.nn.Sigmoid()
    )
    return module


# def BlockusNet2(board):
#     module = tr.nn.Sequential(
#         tr.nn.Flatten(),
#         tr.nn.Linear(7 * len(board) * len(board[0]), 256),
#         tr.nn.Sigmoid(),
#         tr.nn.Linear(256, 64),
#         tr.nn.Sigmoid(),
#         tr.nn.Linear(64, 1),
#     )
#     return module

def calculate_loss(net, x, y_targ):
    y = net(x)
    e  =  tr.sum((y - y_targ)**2)
    return y, e


def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y, e = calculate_loss(net, x, y_targ)
    e.backward()
    optimizer.step()
    return y, e



if __name__ == "__main__":

    # game_set = []
    L, ghosts = pp.smallMaze(2, 5)
    # pos_i, pos_j = 3, 8
    # game_set.append((L1, ghosts_1, pos_i, pos_j))

    # L2, ghosts_2 = pp.bigMaze(1, 3)
    # pos_i, pos_j = 5, 10
    # game_set.append((L2, ghosts_2, pos_i, pos_j))
    #
    # L3, ghosts_3 = pp.smallMaze(1,3)
    # pos_i, pos_j = 3, 8
    # game_set.append((L3, ghosts_3, pos_i, pos_j))
    #
    # L4, ghosts_4 = pp.bigMaze(2,3)
    # pos_i, pos_j = 5, 10
    # game_set.append((L4, ghosts_4, pos_i, pos_j))
    #
    # L5, ghosts_5 = pp.bigMaze(2,5)
    # pos_i, pos_j = 5, 10
    # game_set.append((L5, ghosts_5, pos_i, pos_j))


    net = BlockusNet3(L)
    print(net)

    import pickle as pk
    with open("data_small_2_5.pkl", "rb") as f: (x, y_targ) = pk.load(f)

    # Optimization loop
    print(x[:10] ,y_targ[:10])
    optimizer = tr.optim.Adam(net.parameters())
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 10
    train, test = shuffle[:-split], shuffle[-split:]
    for epoch in range(200):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 50 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle)-split))
        test_loss.append(e_test.item() / split)

    tr.save(net.state_dict(), "model_net3_small_2_5.pth")

    import matplotlib.pyplot as pt
    pt.plot(train_loss,'b-')
    pt.plot(test_loss,'r-')
    pt.legend(["Train","Test"])
    pt.xlabel("Iteration")
    pt.ylabel("Average Loss")
    pt.show()

    pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(),'bo')
    pt.plot(y_test.detach().numpy(), y_targ[test].detach().numpy(),'ro')
    pt.legend(["Train","Test"])
    pt.xlabel("Actual output")
    pt.ylabel("Target output")
    pt.show()













