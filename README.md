# 🧩 8-Puzzle Solver with A* Search Hint Bot

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![UI Library](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)](#)

Aplikasi permainan **8-Puzzle Single-Player** berbasis Python yang dilengkapi dengan bot AI cerdas. Bot ini berfungsi sebagai pemberi petunjuk (*Hint*) langkah tercepat dan paling optimal menuju solusi (*goal state*) menggunakan algoritma **A\* Search** dengan heuristik **Manhattan Distance**. Papan dijamin 100% *solvable* menggunakan verifikasi paritas **Inversion Count**.

> Proyek ini dikembangkan untuk memenuhi Tugas Kelompok Mata Kuliah **Kecerdasan Tiruan**.

---

## 🛠️ Tech Stack & Perkakas

- **Bahasa Pemrograman:** Python 3.10+
- **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (v5.2.2) & Colorama (v0.4.6)
- **Algoritma & Struktur Data:** A\* Search, Priority Queue (`heapq`), Closed List (`set`), Matriks/Tuple $3 \times 3$
- **IDE & Tools:** Visual Studio Code (Ekstensi: *Python*, *Pylance*, *Git Graph*, *Markdown PDF*)
- **Version Control & Env:** Git, GitHub, dan Python Virtual Environment (`venv`)

---

## 👥 Kelompok & Pembagian Jobdesk (*End-to-End Ownership*)

Setiap anggota memiliki tanggung jawab terintegrasi mulai dari fase implementasi kode program (*coding*) hingga penyusunan bab laporan:

| Anggota & Role | Branch Git | Fase Produksi (Coding & Engine) | Fase Pasca-Produksi (Laporan Dokumen) |
|:---|:---|:---|:---|
| **Anggota 1**<br>*(AI Specialist)*<br>*(I Made Sheva Virgantara Natha Parsha)* | `feature/ai-engine` | • Mengembangkan algoritma A\* Search (`src/ai_engine.py`)<br>• Menghitung estimasi Manhattan Distance<br>• Mengelola Priority Queue & Closed List<br>• Ekstraksi 1 langkah terbaik untuk Hint | • Menulis **Bab II Landasan Teori AI**<br>• Formulasi matematis $f(n) = g(n) + h(n)$<br>• Penyusunan Pseudocode / Flowchart A\*<br>• Analisis kompleksitas algoritma $\mathcal{O}(b^d)$ |
| **Anggota 2**<br>*(Logic Engineer)* | `feature/game-logic` | • Matriks papan $3 \times 3$ (`src/game_logic.py`)<br>• Operator pergerakan ubin (Up, Down, Left, Right)<br>• Checker paritas Inversion Count<br>• Generator papan acak terjamin *solvable* | • Menulis **Bab III Perancangan Sistem**<br>• Pemetaan ruang keadaan (*State-Space*)<br>• Aturan transisi & operator pergerakan<br>• Teorema matematika solvabilitas papan |
| **Anggota 3**<br>*(UI/UX Specialist)* | `feature/ui-interface` | • Antarmuka visual GUI (`src/ui_interface.py`)<br>• Input Handler pergerakan manual<br>• Display visual rekomendasi Hint<br>• Tampilan layar kemenangan (*Victory Screen*) | • Menulis **Bab IV Rancangan Antarmuka**<br>• *Screenshot* & alur permainan<br>• Deskripsi komponen visual GUI<br>• Panduan pengguna (*User Manual*) |
| **Anggota 4**<br>*(Integrator & QA Lead)*<br>*(Muhammad Izzanurdin Hasan)* | `feature/integration` | • Integrasi seluruh modul (`src/main.py`)<br>• Error handling & guard input<br>• Pembuatan sampel test case (`tests/test_cases.py`)<br>• Benchmark kecepatan respon A\* | • Menulis **Bab I, V, VI Laporan**<br>• Tabel pengujian *Black-Box Testing*<br>• Grafik/tabel waktu eksekusi A\* (ms)<br>• Formatting & kompilasi dokumen akhir |

---

## 📁 Struktur Direktori

```text
8-puzzle-solver-bot-kecerdasantiruan-i-kelompok1/
├── src/
│   ├── main.py             # Titik masuk utama aplikasi (Entry Point)
│   ├── ai_engine.py        # Implementasi A* Search & Heuristik Manhattan Distance
│   ├── game_logic.py       # Logika papan, transisi state, dan solvability checker
│   └── ui_interface.py     # Desain GUI interaktif menggunakan CustomTkinter
├── tests/
│   └── test_cases.py       # Unit testing & skenario benchmark performa
├── .gitignore              # Konfigurasi file yang diabaikan Git
├── requirements.txt        # Daftar dependensi pustaka Python
├── READMEE.md              # Dokumen ringkas briefing tim / cetak PDF
└── README.md               # Dokumentasi utama repositori
```

---

## 🚀 Panduan Setup Environment Step-by-Step

Ikuti langkah-langkah berikut untuk menyiapkan environment pengembangan di komputer lokal:

### 1. Clone Repositori
Buka terminal atau Command Prompt, lalu jalankan:

```bash
git clone https://github.com/Izzanurdin/8-puzzle-solver-bot-kecerdasantiruan-i-kelompok1.git
cd 8-puzzle-solver-bot-kecerdasantiruan-i-kelompok1
```

### 2. Buat & Aktifkan Virtual Environment (`venv`)

Pilih perintah sesuai sistem operasi dan terminal yang Anda gunakan:

- **Windows (Git Bash):**
  ```bash
  python -m venv venv
  source venv/Scripts/activate
  ```

- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(Jika muncul error Execution Policy, jalankan `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` terlebih dahulu)*

- **Windows (Command Prompt / CMD):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```

- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

> 💡 **Indikator Berhasil:** Akan muncul tanda `(venv)` di sebelah kiri prompt terminal Anda.

### 3. Instalasi Dependensi
Pastikan `venv` sudah aktif, kemudian jalankan:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💻 Cara Menjalankan Aplikasi

*(Status: **Dalam Pengembangan**)*

Setelah semua modul terintegrasi di branch `main`, aplikasi dapat dijalankan melalui perintah:

```bash
python src/main.py
```

---

## 🧠 Konsep & Algoritma

1. **8-Puzzle Problem**: Permainan sliding puzzle $3 \times 3$ yang terdiri dari 8 ubin berangka 1 sampai 8 serta satu ruang kosong (blank tile).
2. **Solvability Check**: Memastikan susunan papan awal dapat dipecahkan dengan menghitung jumlah inversi (*inversion count*). Jika genap, papan dijamin solvable.
3. **A\* Search Algorithm**:
   $$f(n) = g(n) + h(n)$$
   - $g(n)$: Biaya langkah dari *initial state* ke *state* saat ini.
   - $h(n)$: Estimasi biaya dari *state* saat ini ke *goal state* menggunakan **Manhattan Distance**.
4. **Manhattan Distance**:
   $$h(n) = \sum (|x_{current} - x_{goal}| + |y_{current} - y_{goal}|)$$
   Heuristik ini bersifat *admissible* (tidak pernah melebih-lebihkan jarak aktual) dan *consistent*, menjamin rute yang dihasilkan selalu optimal.

---

## ✅ Checklist Jobdesk Masing-Masing Anggota

### 🧑‍💻 Anggota 1 — AI & Heuristic Specialist (`feature/ai-engine`)
- [ ] `[Coding]` Fungsi `calculate_manhattan_distance(state)` pada `src/ai_engine.py`
- [ ] `[Coding]` Algoritma `a_star_search(initial_state)` menggunakan `heapq`
- [ ] `[Coding]` Fungsi `get_hint(state)` penentu 1 langkah terbaik
- [ ] `[Laporan]` Bab II Landasan Teori AI ($f(n) = g(n) + h(n)$, Manhattan Distance, Flowchart A\*, Kompleksitas $\mathcal{O}(b^d)$)

### ⚙️ Anggota 2 — Game Logic Engineer (`feature/game-logic`)
- [ ] `[Coding]` Matriks papan $3 \times 3$ dan `GOAL_STATE` pada `src/game_logic.py`
- [ ] `[Coding]` Fungsi `get_inversion_count(state)` dan `is_solvable(state)`
- [ ] `[Coding]` Fungsi `generate_random_board()` terjamin *solvable*
- [ ] `[Coding]` Fungsi `get_neighbors(state)` untuk operator pergerakan ubin (Up, Down, Left, Right)
- [ ] `[Laporan]` Bab III Perancangan Sistem (*State-Space*, aturan transisi, teorema solvabilitas papan)

### 🎨 Anggota 3 — UI/UX Specialist (`feature/ui-interface`)
- [ ] `[Coding]` Kelas `PuzzleUI` menggunakan CustomTkinter pada `src/ui_interface.py`
- [ ] `[Coding]` Layout grid $3 \times 3$, label status Hint, dan tombol aksi (*New Game*, *Reset*, *Hint*)
- [ ] `[Coding]` Method `update_board(state)` dan `set_hint_text(text)`
- [ ] `[Coding]` Tampilan layar kemenangan (*Victory Screen*)
- [ ] `[Laporan]` Bab IV Rancangan Antarmuka (*Screenshot* UI, komponen visual, *User Manual*)

### 🛡️ Anggota 4 — System Integrator & QA Lead (`feature/integration`)
- [ ] `[Coding]` Menyambungkan seluruh modul pada `src/main.py`
- [ ] `[Coding]` Menambahkan *error handling* dan *guard input*
- [ ] `[Coding]` Membuat berkas pengujian otomatis `tests/test_cases.py`
- [ ] `[Laporan]` Bab I Pendahuluan
- [ ] `[Laporan]` Bab V Pengujian & Analisis (*Black-Box Testing* & grafik/tabel benchmark respon A\*)
- [ ] `[Laporan]` Bab VI Penutup & Kesimpulan
- [ ] `[Laporan]` Kompilasi dan *formatting* akhir dokumen laporan

---

## 📌 Tracker Progres Modul

| Fitur / Sub-Sistem | PJ (Anggota) | Status | Catatan |
|:---|:---:|:---:|:---|
| Inisialisasi Project & Environment | Izza | 🟢 Selesai | Repositori, `venv`, & starter code siap |
| Game Logic & Solvability Checker | Anggota 2 | 🟡 In Progress | Pembuatan matriks papan & inversion count |
| A\* Engine & Manhattan Distance | Anggota 1 | 🟡 In Progress | Algoritma pencarian rute terpendek |
| Desain Antarmuka GUI (CustomTkinter) | Anggota 3 | 🟡 In Progress | Pembuatan grid papan & tombol interaktif |
| Integrasi Controller & Event Handler | Izza | 🔴 Belum Mulai | Menyambungkan UI dengan Logic & AI Engine |
| Testing & Benchmark Skenario | Izza & Tim | 🔴 Belum Mulai | Pengujian tingkat kesulitan & kecepatan A\* |
| Penyusunan Laporan & Dokumentasi | Seluruh Tim | 🔴 Belum Mulai | Penulisan bab laporan sesuai domain |

**Keterangan Status:**
- 🔴 **Belum Mulai**
- 🟡 **In Progress** *(Sedang Dikerjakan)*
- 🟢 **Selesai** *(Merged to Main)*

---

## 🌿 Panduan Branching Git untuk Anggota Tim

> ⚠️ **Aturan Emas:** Dilarang melakukan *commit* atau *push* langsung ke branch `main`.

1. **Pindah ke branch fitur masing-masing:**
   - Anggota 1: `git checkout -b feature/ai-engine`
   - Anggota 2: `git checkout -b feature/game-logic`
   - Anggota 3: `git checkout -b feature/ui-interface`
   - Anggota 4: `git checkout -b feature/integration`
2. **Lakukan commit secara berkala dengan pesan informatif:**
   ```bash
   git add .
   git commit -m "feat: implementasi fungsi pencarian rute terpendek"
   ```
3. **Push branch fitur ke remote repositori:**
   ```bash
   git push -u origin <nama-branch-anda>
   ```
4. **Buat Pull Request (PR)** di GitHub menuju branch `main` untuk direview dan di-merge oleh System Integrator.
