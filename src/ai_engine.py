import heapq

from game_logic import GOAL_STATE, get_neighbors


def calculate_manhattan_distance(state):
    """
    Menghitung Manhattan Distance dari state saat ini
    menuju GOAL_STATE.

    Blank tile (0) tidak dihitung.

    Args:
        state (tuple): State puzzle 8-Puzzle.

    Returns:
        int: Nilai Manhattan Distance.
    """
    distance = 0

    for index, tile in enumerate(state):
        if tile == 0:
            continue

        current_row = index // 3
        current_col = index % 3

        goal_index = GOAL_STATE.index(tile)
        goal_row = goal_index // 3
        goal_col = goal_index % 3

        distance += abs(current_row - goal_row)
        distance += abs(current_col - goal_col)

    return distance


def a_star_search(initial_state):
    """
    Mencari jalur optimal dari initial_state menuju GOAL_STATE
    menggunakan algoritma A*.

    Rumus:
        f(n) = g(n) + h(n)

    Args:
        initial_state (tuple): State awal puzzle.

    Returns:
        list: Jalur state dari initial_state sampai GOAL_STATE.
        None: Jika solusi tidak ditemukan.
    """

    # Jika state awal sudah merupakan goal.
    if initial_state == GOAL_STATE:
        return [initial_state]

    # Priority Queue.
    # Format:
    # (f_score, counter, state)
    open_list = []

    # Counter digunakan sebagai tie-breaker ketika
    # terdapat state dengan f_score yang sama.
    counter = 0

    # g_score menyimpan cost dari initial state
    # menuju setiap state.
    g_score = {
        initial_state: 0
    }

    # Menyimpan parent setiap state untuk
    # melakukan rekonstruksi path.
    came_from = {}

    # Closed List menyimpan state yang sudah diproses.
    closed_list = set()

    # Heuristic state awal.
    initial_h = calculate_manhattan_distance(initial_state)

    # g(initial_state) = 0
    # sehingga f(initial_state) = 0 + h(initial_state)
    initial_f = initial_h

    heapq.heappush(
        open_list,
        (initial_f, counter, initial_state)
    )

    while open_list:

        # Mengambil state dengan f_score terkecil.
        _, _, current_state = heapq.heappop(open_list)

        # Jika state sudah diproses sebelumnya,
        # jangan diproses kembali.
        if current_state in closed_list:
            continue

        # Jika mencapai goal, rekonstruksi path.
        if current_state == GOAL_STATE:
            path = [current_state]

            while current_state in came_from:
                current_state = came_from[current_state]
                path.append(current_state)

            path.reverse()
            return path

        # Tandai state sebagai sudah diproses.
        closed_list.add(current_state)

        # get_neighbors() mengembalikan:
        # (move, neighbor_state)
        neighbors = get_neighbors(current_state)

        for _, neighbor in neighbors:

            # Jangan memproses state yang sudah berada
            # di Closed List.
            if neighbor in closed_list:
                continue

            # Setiap perpindahan tile memiliki cost 1.
            tentative_g = g_score[current_state] + 1

            # Jika neighbor belum ditemukan sebelumnya
            # atau ditemukan jalur yang lebih murah.
            if (
                neighbor not in g_score
                or tentative_g < g_score[neighbor]
            ):
                came_from[neighbor] = current_state
                g_score[neighbor] = tentative_g

                # h(n) = Manhattan Distance.
                h_score = calculate_manhattan_distance(neighbor)

                # f(n) = g(n) + h(n).
                f_score = tentative_g + h_score

                counter += 1

                heapq.heappush(
                    open_list,
                    (f_score, counter, neighbor)
                )

    # Tidak ditemukan solusi.
    return None


def get_hint(state):
    """
    Mengambil satu langkah terbaik dari state saat ini.

    A* digunakan untuk mencari path optimal.
    Hint yang dikembalikan adalah arah gerakan pertama.

    Args:
        state (tuple): State puzzle saat ini.

    Returns:
        str: Arah gerakan terbaik:
             "Up", "Down", "Left", atau "Right".
        None: Jika state sudah goal atau solusi tidak ditemukan.
    """

    # Cari path optimal menggunakan A*.
    path = a_star_search(state)

    # Jika tidak ada solusi atau state sudah goal.
    if path is None or len(path) < 2:
        return None

    # State pertama = state saat ini.
    current_state = path[0]

    # State kedua = state hasil langkah optimal pertama.
    next_state = path[1]

    # Cari semua kemungkinan gerakan dari state saat ini.
    neighbors = get_neighbors(current_state)

    # Cari arah yang menghasilkan next_state.
    for move, neighbor in neighbors:
        if neighbor == next_state:
            return move

    # Seharusnya tidak terjadi jika get_neighbors()
    # bekerja dengan benar.
    return None
