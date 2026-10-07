import customtkinter as ctk
from ui_interface import PuzzleUI

if __name__ == "__main__":
    # 1. Membuat jendela utama (root window)
    root = ctk.CTk()
    
    # 2. Menjalankan PuzzleUI dengan memasukkan root ke dalamnya
    app = PuzzleUI(root)
    
    # 3. Memulai loop aplikasi
    root.mainloop()