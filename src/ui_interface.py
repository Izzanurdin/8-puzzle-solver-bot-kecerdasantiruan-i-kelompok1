import customtkinter as ctk
import random


class PuzzleUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ============================================================
        # KONFIGURASI WINDOW
        # ============================================================
        self.title("8-Puzzle Solver")
        self.geometry("650x750")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ============================================================
        # STATE SEMENTARA
        # 0 = kotak kosong
        #
        # 🔗 CONNECTION TO GAME LOGIC
        # Nanti state ini akan berasal dari:
        # src/game_logic.py
        #
        # Jangan mengganti bagian ini sebelum game_logic.py
        # dari anggota lain sudah tersedia.
        # ============================================================
        self.initial_state = (
            1, 2, 3,
            4, 5, 6,
            7, 8, 0
        )

        self.current_state = list(self.initial_state)

        # ============================================================
        # STATE UI
        # ============================================================
        self.buttons = []

        # ============================================================
        # JUDUL
        # ============================================================
        self.title_label = ctk.CTkLabel(
            self,
            text="8-PUZZLE SOLVER",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        self.title_label.pack(pady=(30, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Susun angka 1 sampai 8 dengan benar",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.pack(pady=(0, 20))

        # ============================================================
        # BOARD
        # ============================================================
        self.board_frame = ctk.CTkFrame(
            self,
            width=450,
            height=450,
            corner_radius=15
        )
        self.board_frame.pack(pady=10)

        self.create_board()

        # ============================================================
        # HINT AREA
        # ============================================================
        self.hint_frame = ctk.CTkFrame(
            self,
            width=500,
            height=70,
            corner_radius=12
        )
        self.hint_frame.pack(pady=(20, 10), padx=30, fill="x")

        self.hint_label = ctk.CTkLabel(
            self.hint_frame,
            text="Hint: Belum ada petunjuk",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.hint_label.pack(pady=18)

        # ============================================================
        # BUTTON AREA
        # ============================================================
        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.button_frame.pack(pady=15)

        self.new_game_button = ctk.CTkButton(
            self.button_frame,
            text="New Game",
            width=140,
            height=40,
            command=self.new_game
        )
        self.new_game_button.grid(row=0, column=0, padx=8)

        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="Reset",
            width=140,
            height=40,
            command=self.reset_game
        )
        self.reset_button.grid(row=0, column=1, padx=8)

        self.hint_button = ctk.CTkButton(
            self.button_frame,
            text="Hint",
            width=140,
            height=40,
            command=self.show_hint
        )
        self.hint_button.grid(row=0, column=2, padx=8)

        # ============================================================
        # STATUS
        # ============================================================
        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Ready",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(pady=5)

    # ================================================================
    # MEMBUAT BOARD 3 x 3
    # ================================================================
    def create_board(self):
        for row in range(3):
            for column in range(3):

                button = ctk.CTkButton(
                    self.board_frame,
                    text="",
                    width=125,
                    height=125,
                    corner_radius=10,
                    font=ctk.CTkFont(size=32, weight="bold"),
                    command=lambda index=row * 3 + column:
                    self.tile_clicked(index)
                )

                button.grid(
                    row=row,
                    column=column,
                    padx=8,
                    pady=8
                )

                self.buttons.append(button)

        self.update_board(self.current_state)

    # ================================================================
    # UPDATE BOARD
    #
    # Method ini nantinya sangat penting untuk integrasi.
    #
    # 🔗 CONNECTION TO GAME LOGIC
    # state akan dikirim oleh game_logic.py.
    #
    # Contoh:
    # ui.update_board(state)
    # ================================================================
    def update_board(self, state):
        self.current_state = list(state)

        for index, value in enumerate(self.current_state):

            if value == 0:
                self.buttons[index].configure(
                    text="",
                    state="disabled"
                )
            else:
                self.buttons[index].configure(
                    text=str(value),
                    state="normal"
                )

    # ================================================================
    # INPUT HANDLER
    #
    # Sementara menggunakan logika lokal.
    #
    # 🔗 CONNECTION TO GAME LOGIC
    # Nantinya perpindahan tile sebaiknya menggunakan:
    #
    # game_logic.py
    #
    # agar aturan pergerakan tetap berada di modul game logic.
    # ================================================================
    def tile_clicked(self, index):

        empty_index = self.current_state.index(0)

        valid_moves = []

        row = index // 3
        column = index % 3

        empty_row = empty_index // 3
        empty_column = empty_index % 3

        if row == empty_row:
            if abs(column - empty_column) == 1:
                valid_moves.append(True)

        if column == empty_column:
            if abs(row - empty_row) == 1:
                valid_moves.append(True)

        if valid_moves:

            self.current_state[index], self.current_state[empty_index] = (
                self.current_state[empty_index],
                self.current_state[index]
            )

            self.update_board(self.current_state)

            self.check_victory()

    # ================================================================
    # NEW GAME
    #
    # 🔗 CONNECTION TO GAME LOGIC
    # Nantinya gunakan:
    #
    # generate_random_board()
    #
    # dari game_logic.py.
    # ================================================================
    def new_game(self):

        numbers = list(range(9))

        while True:
            random.shuffle(numbers)

            # Sementara hanya digunakan untuk UI.
            # Nanti diganti dengan generate_random_board().
            if numbers != list(self.initial_state):
                break

        self.current_state = numbers

        self.update_board(self.current_state)

        self.set_hint_text("Hint: Belum ada petunjuk")
        self.status_label.configure(text="Status: New game")

    # ================================================================
    # RESET GAME
    # ================================================================
    def reset_game(self):

        self.current_state = list(self.initial_state)

        self.update_board(self.current_state)

        self.set_hint_text("Hint: Belum ada petunjuk")
        self.status_label.configure(text="Status: Reset")

    # ================================================================
    # HINT
    #
    # 🔗 CONNECTION TO AI ENGINE
    # Nantinya fungsi ini akan memanggil:
    #
    # get_hint(state)
    #
    # dari ai_engine.py.
    #
    # Contoh konsep:
    #
    # hint = get_hint(self.current_state)
    # self.set_hint_text(hint)
    # ================================================================
    def show_hint(self):

        # ------------------------------------------------------------
        # MOCK HINT
        # Sementara hanya untuk preview UI.
        # ------------------------------------------------------------
        self.set_hint_text(
            "Hint: AI akan memberikan langkah terbaik di sini."
        )

        # 🔗 CONNECTION TO AI ENGINE
        # Ganti bagian mock ini setelah ai_engine.py tersedia.

    # ================================================================
    # SET HINT TEXT
    # ================================================================
    def set_hint_text(self, text):

        self.hint_label.configure(
            text=f"Hint: {text}"
        )

    # ================================================================
    # CHECK VICTORY
    #
    # 🔗 CONNECTION TO GAME LOGIC
    # Nantinya bisa menggunakan GOAL_STATE dari game_logic.py.
    # ================================================================
    def check_victory(self):

        goal_state = [
            1, 2, 3,
            4, 5, 6,
            7, 8, 0
        ]

        if self.current_state == goal_state:
            self.show_victory()

    # ================================================================
    # VICTORY SCREEN
    # ================================================================
    def show_victory(self):

        victory_window = ctk.CTkToplevel(self)

        victory_window.title("Puzzle Solved!")
        victory_window.geometry("400x300")
        victory_window.resizable(False, False)

        title = ctk.CTkLabel(
            victory_window,
            text="🎉 PUZZLE SOLVED!",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(50, 15))

        message = ctk.CTkLabel(
            victory_window,
            text="Selamat! Kamu berhasil menyusun\n"
                 "angka 1 sampai 8 dengan benar.",
            font=ctk.CTkFont(size=15)
        )
        message.pack(pady=10)

        close_button = ctk.CTkButton(
            victory_window,
            text="Continue",
            width=150,
            command=victory_window.destroy
        )
        close_button.pack(pady=20)


# ====================================================================
# PREVIEW UI
#
# Catatan:
# Bagian ini hanya untuk mengetes UI secara mandiri.
#
# 🔗 CONNECTION TO main.py
# Nantinya Anggota 4 dapat mengintegrasikan PuzzleUI melalui:
#
# from ui_interface import PuzzleUI
#
# app = PuzzleUI()
# app.mainloop()
# ====================================================================

if __name__ == "__main__":
    app = PuzzleUI()
    app.mainloop()