# 1. Melakukan 'import' atau memanggil ketiga file yang sudah dibuat
import game_logic
import ai_engine
from ui_interface import PuzzleUI

# 2. Membuat class baru bernama MainApp yang 'mewarisi' semua tampilan PuzzleUI
class MainApp(PuzzleUI):
    def __init__(self):
        # Membangun tampilan dasar yang ada di PuzzleUI
        super().__init__()
        
        # 3. MENGGANTI STATE AWAL
        # Kita panggil pembuat papan acak dari game_logic
        self.initial_state = game_logic.generate_random_board()
        self.current_state = list(self.initial_state)
        # Memperbarui tampilan layar dengan angka yang baru
        self.update_board(self.current_state)

    # 4. MENGGANTI TOMBOL NEW GAME
    # Fungsi ini akan menimpa (override) fungsi new_game bawaan dari ui_interface
    def new_game(self):
        # Minta papan acak baru dari game_logic
        self.initial_state = game_logic.generate_random_board()
        self.current_state = list(self.initial_state)
        self.update_board(self.current_state)

        # Reset tulisan hint di layar
        self.set_hint_text("Belum ada petunjuk")
        self.status_label.configure(text="Status: New game")

    # 5. MENGGANTI TOMBOL HINT
    # Menghubungkan tombol hint dengan otak AI kita
    def show_hint(self):
        self.status_label.configure(text="Status: AI sedang berpikir...")
        self.update() # Memaksa layar untuk memperbarui tulisan status

        # ai_engine butuh format 'tuple' (data yang tidak bisa diubah), jadi kita ubah dulu
        state_sekarang = tuple(self.current_state)

        # Minta petunjuk dari ai_engine
        hint = ai_engine.get_hint(state_sekarang)

        if hint:
            # Jika ketemu langkahnya, tampilkan di layar
            self.set_hint_text(f"Geser kotak kosong ke arah {hint}")
            self.status_label.configure(text="Status: Hint ditemukan!")
        else:
            # Jika tidak ada solusi atau puzzle sudah selesai
            self.set_hint_text("Solusi tidak ditemukan atau puzzle sudah selesai.")
            self.status_label.configure(text="Status: Selesai")

    # 6. MENGGANTI CEK KEMENANGAN
    def check_victory(self):
        # Mengecek apakah susunan angka saat ini sama dengan GOAL_STATE di game_logic
        if tuple(self.current_state) == game_logic.GOAL_STATE:
            self.show_victory()

# 7. MENJALANKAN APLIKASI
# Baris ini memastikan aplikasi hanya berjalan jika file main.py ini ditekan "Run"
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()