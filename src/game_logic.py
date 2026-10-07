import random
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def get_inversion_count(state):
    tiles = [t for t in state if t != 0]
    return sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )git pull