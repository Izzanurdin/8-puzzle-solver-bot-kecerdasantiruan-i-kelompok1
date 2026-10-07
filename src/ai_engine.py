import heapq

from game_logic import GOAL_STATE, get_neighbors


def calculate_manhattan_distance(state):
    """
    Menghitung Manhattan Distance dari state saat ini
    menuju GOAL_STATE.

    Blank tile (0) tidak dihitung.
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

    f(n) = g(n) + h(n)

    Returns:
        list: Jalur state dari initial_state sampai GOAL_STATE.
              Jika tidak ditemukan, mengembalikan None.
    """

    if initial_state == GOAL_STATE:
        return [initial_state]

    # Priority Queue:
    # (f_score, counter, state)
    open_list = []

    # Counter digunakan sebagai tie-breaker ketika
    # dua state memiliki f_score yang sama.
    counter = 0

    # g_score menyimpan biaya dari initial state
    # menuju state tertentu.
    g_score = {initial_state: 0}

    # Menyimpan parent setiap state untuk membangun kembali path.
    came_from = {}

    # Closed List
    closed_list = set()

    # Heuristic initial state
    initial_h = calculate_manhattan_distance(initial_state)

    # f(n) = g(n) + h(n)
    initial_f = initial_h

    heapq.heappush(
        open_list,
        (initial_f, counter, initial_state)
    )

    while open_list:

        # Ambil state dengan f(n) terkecil
        _, _, current_state = heapq.heappop(open_list)

        # Jika state sudah pernah diproses, lewati
        if current_state in closed_list:
            continue

        # Jika sudah mencapai goal
        if current_state == GOAL_STATE:
            path = [current_state]

            while current_state in came_from:
                current_state = came_from[current_state]
                path.append(current_state)

            path.reverse()
            return path

        # Masukkan state ke Closed List
        closed_list.add(current_state)

        # Ambil semua state tetangga
        neighbors = get_neighbors(current_state)

        for direction, neighbor in neighbors:
            
            # Jangan memproses state yang sudah selesai
            if neighbor in closed_list:
                continue

            # Biaya menuju neighbor
            tentative_g = g_score[current_state] + 1

            # Jika neighbor belum pernah ditemukan
            # atau ditemukan jalur yang lebih murah
            if (
                neighbor not in g_score
                or tentative_g < g_score[neighbor]
            ):
                came_from[neighbor] = current_state
                g_score[neighbor] = tentative_g

                h_score = calculate_manhattan_distance(neighbor)
                f_score = tentative_g + h_score

                counter += 1

                heapq.heappush(
                    open_list,
                    (f_score, counter, neighbor)
                )

    # Tidak ditemukan solusi
    return None


def get_hint(state):
    """
    Mengambil satu langkah terbaik dari state saat ini.

    Returns:
        tuple: State berikutnya yang merupakan langkah optimal.
        None: Jika tidak ditemukan solusi atau state sudah goal.
    """

    path = a_star_search(state)

    if path is None or len(path) < 2:
        return None

    return path[1]