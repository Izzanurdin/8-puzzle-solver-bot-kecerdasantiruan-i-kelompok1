import random
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def get_inversion_count(state):
    tiles = [t for t in state if t != 0]
    return sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )

def is_solvable(state):
    return get_inversion_count(state) % 2 == 0

def generate_random_board():
    while True:
        tiles = list(range(9))
        random.shuffle(tiles)
        state = tuple(tiles)
        if is_solvable(state) and state != GOAL_STATE:
            return state

def get_neighbors(state):
    """Mengembalikan list (arah_ubin_kosong, state_baru)."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
    result = []
    for name, (dr, dc) in moves.items():
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            target = r * 3 + c
            new_state = list(state)
            new_state[blank], new_state[target] = new_state[target], new_state[blank]
            result.append((name, tuple(new_state)))
    return result