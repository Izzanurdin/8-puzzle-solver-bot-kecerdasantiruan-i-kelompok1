import sys
import os
import time
import random
import heapq

# Membantu Python menemukan folder 'src' agar bisa memanggil file teman-temanmu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import game_logic
import ai_engine

def generate_board_by_difficulty(scramble_moves):
    """
    Membuat puzzle dengan tingkat kesulitan spesifik.
    Caranya: Mulai dari GOAL_STATE, lalu jalan mundur secara acak sebanyak 'scramble_moves'.
    """
    state = game_logic.GOAL_STATE
    prev_state = None
    
    for _ in range(scramble_moves):
        # Ambil semua kemungkinan gerakan
        neighbors = game_logic.get_neighbors(state)
        # Cegah ubin kembali ke posisi sebelumnya agar benar-benar teracak
        valid_moves = [n[1] for n in neighbors if n[1] != prev_state]
        
        prev_state = state
        state = random.choice(valid_moves)
        
    return state

def a_star_benchmark(initial_state):
    """
    Mesin A* khusus pengujian. 
    Sama persis dengan ai_engine, namun ditambah fitur penghitung 'nodes_expanded'.
    """
    if initial_state == game_logic.GOAL_STATE:
        return [initial_state], 0

    open_list = []
    counter = 0
    g_score = {initial_state: 0}
    came_from = {}
    closed_list = set()
    
    initial_h = ai_engine.calculate_manhattan_distance(initial_state)
    heapq.heappush(open_list, (initial_h, counter, initial_state))
    
    nodes_expanded = 0  # VARIABEL PENGHITUNG NODE
    
    while open_list:
        _, _, current_state = heapq.heappop(open_list)
        
        if current_state in closed_list:
            continue
            
        # Setiap kali AI memeriksa kotak baru, catat!
        nodes_expanded += 1
        
        if current_state == game_logic.GOAL_STATE:
            path = [current_state]
            while current_state in came_from:
                current_state = came_from[current_state]
                path.append(current_state)
            path.reverse()
            return path, nodes_expanded
            
        closed_list.add(current_state)
        
        for _, neighbor in game_logic.get_neighbors(current_state):
            if neighbor in closed_list:
                continue
            
            tentative_g = g_score[current_state] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current_state
                g_score[neighbor] = tentative_g
                h_score = ai_engine.calculate_manhattan_distance(neighbor)
                f_score = tentative_g + h_score
                
                counter += 1
                heapq.heappush(open_list, (f_score, counter, neighbor))
                
    return None, nodes_expanded

def run_performance_test():
    """
    Menjalankan pengujian untuk 3 tingkat kesulitan dan mencetak hasilnya.
    """
    print("="*60)
    print("MAMULAI BENCHMARK PERFORMA A* SEARCH")
    print("="*60)
    
    # Skenario sesuai Tabel 5.2 di Laporan
    scenarios = [
        {"kategori": "Mudah", "acak_mundur": 6},
        {"kategori": "Sedang", "acak_mundur": 14},
        {"kategori": "Sangat Sulit", "acak_mundur": 24}
    ]
    
    for sc in scenarios:
        print(f"\nMenyiapkan Papan Kategori: {sc['kategori']}...")
        test_board = generate_board_by_difficulty(sc['acak_mundur'])
        
        # Mulai Stopwatch (perf_counter sangat akurat untuk milidetik)
        start_time = time.perf_counter()
        
        # Jalankan algoritma A*
        path, nodes = a_star_benchmark(test_board)
        
        # Matikan Stopwatch
        end_time = time.perf_counter()
        
        # Kalkulasi hasil
        execution_time_ms = (end_time - start_time) * 1000
        jarak_kedalaman = len(path) - 1 if path else 0
        
        # Tampilkan hasil untuk di-copy ke Laporan
        print(f"-> Jarak Kedalaman Solusi (d): {jarak_kedalaman} langkah")
        print(f"-> Node Diekspansi         : {nodes} node")
        print(f"-> Waktu Eksekusi          : {execution_time_ms:.2f} ms")

if __name__ == "__main__":
    run_performance_test()