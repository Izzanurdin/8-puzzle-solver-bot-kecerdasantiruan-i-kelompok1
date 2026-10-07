import customtkinter as ctk

# ============================================================
# 🔗 CONNECTION TO GAME LOGIC
# File: game_logic.py
# ============================================================
from game_logic import GOAL_STATE, generate_random_board, get_neighbors


# ============================================================
# 🔗 CONNECTION TO AI ENGINE
# File: ai_engine.py
# ============================================================
from ai_engine import get_hint


class PuzzleUI:
    def __init__(self, root):
        self.root = root

        # ====================================================
        # WINDOW
        # ====================================================
        self.root.title("8-Puzzle • A* Hint Bot")
        self.root.geometry("720x820")
        self.root.minsize(650, 760)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ====================================================
        # COLOR PALETTE
        # ====================================================
        self.bg_color = "#0F1117"
        self.card_color = "#171A23"
        self.tile_color = "#242936"
        self.tile_hover = "#303746"

        self.accent_color = "#4F8CFF"
        self.accent_hover = "#3D78E8"

        self.text_primary = "#F5F7FA"
        self.text_secondary = "#9AA4B2"

        self.success_color = "#3DDC97"
        self.warning_color = "#FFCA5C"

        self.root.configure(fg_color=self.bg_color)

        # ====================================================
        # GAME DATA
        # ====================================================
        self.current_state = GOAL_STATE
        self.moves = 0
        self.hint_tile_index = None
        self.game_running = False

        # Timer
        self.elapsed_seconds = 0
        self.timer_job = None

        # Tile buttons
        self.tile_buttons = []

        # ====================================================
        # BUILD UI
        # ====================================================
        self.build_header()
        self.build_stats()
        self.build_board()
        self.build_hint_panel()
        self.build_controls()
        self.build_status()

        self.new_game()

    # ========================================================
    # HEADER
    # ========================================================
    def build_header(self):
        header = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=32,
            pady=(28, 8)
        )

        title = ctk.CTkLabel(
            header,
            text="8-PUZZLE",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=30,
                weight="bold"
            ),
            text_color=self.text_primary
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="A* SEARCH  •  HINT BOT",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold"
            ),
            text_color=self.accent_color
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    # ========================================================
    # STATISTICS
    # ========================================================
    def build_stats(self):
        stats_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        stats_frame.pack(
            fill="x",
            padx=32,
            pady=(8, 12)
        )

        moves_card = self.create_stat_card(
            stats_frame,
            "MOVES",
            "0"
        )
        moves_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )
        self.moves_value = moves_card.value_label

        timer_card = self.create_stat_card(
            stats_frame,
            "TIME",
            "00:00"
        )
        timer_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=6
        )
        self.timer_value = timer_card.value_label

        goal_card = self.create_stat_card(
            stats_frame,
            "GOAL",
            "1 → 8"
        )
        goal_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(6, 0)
        )

    def create_stat_card(self, parent, title, value):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=14,
            height=72
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=self.text_secondary
        )
        title_label.pack(
            anchor="w",
            padx=16,
            pady=(10, 0)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=self.text_primary
        )
        value_label.pack(
            anchor="w",
            padx=16,
            pady=(0, 8)
        )

        card.value_label = value_label

        return card

    # ========================================================
    # BOARD
    # ========================================================
    def build_board(self):
        board_container = ctk.CTkFrame(
            self.root,
            fg_color=self.card_color,
            corner_radius=20
        )
        board_container.pack(
            padx=32,
            pady=10
        )

        board_title = ctk.CTkLabel(
            board_container,
            text="PUZZLE BOARD",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.text_secondary
        )
        board_title.pack(
            pady=(16, 8)
        )

        self.board_frame = ctk.CTkFrame(
            board_container,
            fg_color="transparent"
        )
        self.board_frame.pack(
            padx=18,
            pady=(0, 18)
        )

        for index in range(9):
            button = ctk.CTkButton(
                self.board_frame,
                text="",
                width=105,
                height=105,
                corner_radius=16,
                fg_color=self.tile_color,
                hover_color=self.tile_hover,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=30,
                    weight="bold"
                ),
                border_width=0,
                command=lambda i=index: self.tile_clicked(i)
            )

            row = index // 3
            col = index % 3

            button.grid(
                row=row,
                column=col,
                padx=5,
                pady=5
            )

            self.tile_buttons.append(button)

    # ========================================================
    # HINT PANEL
    # ========================================================
    def build_hint_panel(self):
        self.hint_frame = ctk.CTkFrame(
            self.root,
            fg_color="#151D2D",
            corner_radius=16,
            border_width=1,
            border_color="#263653"
        )
        self.hint_frame.pack(
            fill="x",
            padx=32,
            pady=(8, 8)
        )

        hint_header = ctk.CTkLabel(
            self.hint_frame,
            text="💡  A* HINT",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.accent_color
        )
        hint_header.pack(
            anchor="w",
            padx=18,
            pady=(13, 2)
        )

        self.hint_label = ctk.CTkLabel(
            self.hint_frame,
            text="Tekan HINT untuk mendapatkan langkah terbaik.",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.text_primary,
            wraplength=600,
            justify="left"
        )
        self.hint_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 13)
        )

    # ========================================================
    # CONTROL BUTTONS
    # ========================================================
    def build_controls(self):
        controls = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        controls.pack(
            fill="x",
            padx=32,
            pady=(6, 4)
        )

        self.new_game_button = ctk.CTkButton(
            controls,
            text="NEW GAME",
            height=46,
            corner_radius=12,
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.new_game
        )
        self.new_game_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.hint_button = ctk.CTkButton(
            controls,
            text="💡 HINT",
            height=46,
            corner_radius=12,
            fg_color="#252B38",
            hover_color="#323A4A",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.show_hint
        )
        self.hint_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        self.reset_button = ctk.CTkButton(
            controls,
            text="RESET",
            height=46,
            corner_radius=12,
            fg_color="#252B38",
            hover_color="#323A4A",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.reset_game
        )
        self.reset_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

    # ========================================================
    # STATUS
    # ========================================================
    def build_status(self):
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Status: Ready",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=self.text_secondary
        )
        self.status_label.pack(
            pady=(5, 18)
        )

    # ========================================================
    # NEW GAME
    # 🔗 CONNECTION TO GAME LOGIC
    # ========================================================
    def new_game(self):
        self.stop_timer()

        self.current_state = generate_random_board()

        self.moves = 0
        self.elapsed_seconds = 0
        self.hint_tile_index = None
        self.game_running = True

        self.update_stats()
        self.clear_hint()
        self.update_board(self.current_state)

        self.status_label.configure(
            text="Status: Game dimulai • Susun angka 1–8",
            text_color=self.text_secondary
        )

        self.start_timer()

    # ========================================================
    # RESET GAME
    # ========================================================
    def reset_game(self):
        self.stop_timer()

        self.moves = 0
        self.elapsed_seconds = 0
        self.hint_tile_index = None
        self.game_running = True

        self.update_stats()
        self.clear_hint()
        self.update_board(self.current_state)

        self.status_label.configure(
            text="Status: Puzzle di-reset",
            text_color=self.text_secondary
        )

        self.start_timer()

    # ========================================================
    # UPDATE BOARD
    # ========================================================
    def update_board(self, state):
        self.current_state = tuple(state)

        for index, tile in enumerate(self.current_state):
            button = self.tile_buttons[index]

            if tile == 0:
                button.configure(
                    text="",
                    fg_color="#10131A",
                    hover_color="#10131A",
                    state="disabled"
                )

            else:
                # ====================================================
                # HIGHLIGHT HANYA TILE YANG HARUS DIGESER
                # ====================================================
                if index == self.hint_tile_index:
                    button.configure(
                        text=str(tile),
                        fg_color=self.warning_color,
                        hover_color="#E5B54E",
                        text_color="#111111",
                        state="normal"
                    )
                else:
                    button.configure(
                        text=str(tile),
                        fg_color=self.tile_color,
                        hover_color=self.tile_hover,
                        text_color=self.text_primary,
                        state="normal"
                    )

        self.root.update_idletasks()

    # ========================================================
    # TILE CLICK
    # 🔗 CONNECTION TO GAME LOGIC
    # ========================================================
    def tile_clicked(self, index):
        if not self.game_running:
            return

        if self.current_state[index] == 0:
            return

        neighbors = get_neighbors(self.current_state)

        for direction, new_state in neighbors:

            if new_state[index] == 0:

                opposite_direction = {
                    "Up": "Down",
                    "Down": "Up",
                    "Left": "Right",
                    "Right": "Left"
                }

                tile_number = self.current_state[index]
                player_direction = opposite_direction[direction]

                self.current_state = new_state
                self.moves += 1

                self.hint_tile_index = None

                self.update_stats()
                self.update_board(self.current_state)

                self.status_label.configure(
                    text=(
                        f"Status: Tile {tile_number} "
                        f"digeser {player_direction}"
                    ),
                    text_color=self.text_secondary
                )

                self.clear_hint()

                if self.current_state == GOAL_STATE:
                    self.game_won()
                else:
                    self.game_running = True

                return

    # ========================================================
    # HINT
    # 🔗 CONNECTION TO AI ENGINE
    # ========================================================
    def show_hint(self):
        if not self.game_running:
            return

        current_state = tuple(self.current_state)

        # AI memberikan state setelah satu langkah optimal
        next_state = get_hint(current_state)

        if next_state is None:
            self.hint_label.configure(
                text="⚠ Tidak ditemukan langkah solusi.",
                text_color=self.warning_color
            )
            return

        next_state = tuple(next_state)

        # ====================================================
        # JIKA SUDAH SELESAI
        # ====================================================
        if current_state == GOAL_STATE:
            self.hint_label.configure(
                text="✓ Puzzle sudah selesai!",
                text_color=self.success_color
            )
            return

        # ====================================================
        # CARI POSISI BLANK
        # ====================================================
        current_blank = current_state.index(0)
        next_blank = next_state.index(0)

        current_row, current_col = divmod(
            current_blank,
            3
        )

        next_row, next_col = divmod(
            next_blank,
            3
        )

        # ====================================================
        # PENTING:
        #
        # next_blank adalah posisi tempat BLANK berpindah.
        #
        # Tile yang harus digeser justru adalah tile yang
        # berada di posisi next_blank PADA current_state.
        #
        # Contoh:
        #
        # current:
        # 1 2 3
        # 4 5 0
        # 7 8 6
        #
        # next:
        # 1 2 3
        # 4 5 6
        # 7 8 0
        #
        # next_blank = posisi tile 6
        # maka tile yang harus digeser = 6
        # ====================================================

        tile_index = next_blank
        tile_number = current_state[tile_index]

        # ====================================================
        # TENTUKAN ARAH TILE
        #
        # Perhatian:
        # arah blank = kebalikan arah tile.
        # ====================================================
        if next_row < current_row:
            # Blank bergerak ke atas
            # Tile bergerak ke bawah
            direction = "bawah"
            arrow = "↓"

        elif next_row > current_row:
            # Blank bergerak ke bawah
            # Tile bergerak ke atas
            direction = "atas"
            arrow = "↑"

        elif next_col < current_col:
            # Blank bergerak ke kiri
            # Tile bergerak ke kanan
            direction = "kanan"
            arrow = "→"

        elif next_col > current_col:
            # Blank bergerak ke kanan
            # Tile bergerak ke kiri
            direction = "kiri"
            arrow = "←"

        else:
            return

        # ====================================================
        # SIMPAN POSISI TILE YANG BENAR
        #
        # BUKAN current_blank
        # BUKAN next_blank sebagai blank
        #
        # next_blank adalah posisi TILE yang harus digeser
        # pada current_state.
        # ====================================================
        self.hint_tile_index = tile_index

        # Update board DENGAN current_state
        # supaya tile yang disorot tetap berada pada posisi
        # sebelum pemain melakukan gerakan.
        self.update_board(current_state)

        # ====================================================
        # TAMPILKAN HINT
        # ====================================================
        self.hint_label.configure(
            text=(
                f"Geser tile {tile_number} "
                f"{arrow} ke {direction}\n"
                f"Tile {tile_number} ditandai pada board."
            ),
            text_color=self.text_primary
        )

        self.status_label.configure(
            text=(
                f"Status: Hint aktif • "
                f"Geser tile {tile_number} {direction}"
            ),
            text_color=self.accent_color
        )

    # ========================================================
    # CLEAR HINT
    # ========================================================
    def clear_hint(self):
        self.hint_tile_index = None

        self.hint_label.configure(
            text="Tekan HINT untuk mendapatkan langkah terbaik.",
            text_color=self.text_primary
        )

        if hasattr(self, "tile_buttons"):
            self.update_board(self.current_state)

    # ========================================================
    # STATS
    # ========================================================
    def update_stats(self):
        self.moves_value.configure(
            text=str(self.moves)
        )

        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60

        self.timer_value.configure(
            text=f"{minutes:02d}:{seconds:02d}"
        )

    # ========================================================
    # TIMER
    # ========================================================
    def start_timer(self):
        self.stop_timer()

        if self.game_running:
            self.timer_job = self.root.after(
                1000,
                self.update_timer
            )

    def update_timer(self):
        if not self.game_running:
            return

        self.elapsed_seconds += 1
        self.update_stats()

        self.timer_job = self.root.after(
            1000,
            self.update_timer
        )

    def stop_timer(self):
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass

            self.timer_job = None

    # ========================================================
    # VICTORY
    # ========================================================
    def game_won(self):
        self.game_running = False
        self.stop_timer()

        self.hint_tile_index = None
        self.update_board(self.current_state)

        self.status_label.configure(
            text="Status: Puzzle berhasil diselesaikan! 🎉",
            text_color=self.success_color
        )

        self.show_victory_screen()

    # ========================================================
    # VICTORY SCREEN
    # ========================================================
    def show_victory_screen(self):
        overlay = ctk.CTkToplevel(self.root)
        overlay.title("Puzzle Complete")
        overlay.geometry("430x430")
        overlay.resizable(False, False)

        overlay.configure(
            fg_color=self.bg_color
        )

        overlay.transient(self.root)
        overlay.grab_set()

        container = ctk.CTkFrame(
            overlay,
            fg_color=self.card_color,
            corner_radius=24
        )
        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        trophy = ctk.CTkLabel(
            container,
            text="🏆",
            font=ctk.CTkFont(size=54)
        )
        trophy.pack(pady=(35, 5))

        title = ctk.CTkLabel(
            container,
            text="PUZZLE SOLVED!",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color=self.success_color
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            container,
            text=(
                "Great job! Kamu berhasil menyusun\n"
                "semua angka dengan benar."
            ),
            font=ctk.CTkFont(size=13),
            text_color=self.text_secondary,
            justify="center"
        )
        subtitle.pack(pady=(8, 20))

        result_frame = ctk.CTkFrame(
            container,
            fg_color="#10131A",
            corner_radius=14
        )
        result_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )

        result = ctk.CTkLabel(
            result_frame,
            text=(
                f"Moves   {self.moves}\n"
                f"Time    {self.format_time()}"
            ),
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=self.text_primary,
            justify="center"
        )
        result.pack(pady=16)

        play_again = ctk.CTkButton(
            container,
            text="PLAY AGAIN",
            height=45,
            corner_radius=12,
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=lambda: self.close_victory_and_new_game(
                overlay
            )
        )
        play_again.pack(
            fill="x",
            padx=30,
            pady=(15, 8)
        )

        close_button = ctk.CTkButton(
            container,
            text="CLOSE",
            height=40,
            corner_radius=12,
            fg_color="#252B38",
            hover_color="#323A4A",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=overlay.destroy
        )
        close_button.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

    # ========================================================
    # VICTORY HELPERS
    # ========================================================
    def format_time(self):
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60

        return f"{minutes:02d}:{seconds:02d}"

    def close_victory_and_new_game(self, overlay):
        overlay.destroy()
        self.new_game()


# ============================================================
# RUN UI
# ============================================================
if __name__ == "__main__":
    root = ctk.CTk()

    app = PuzzleUI(root)

    root.mainloop()