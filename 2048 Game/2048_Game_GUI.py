"""
2048 - Full GUI (Tkinter) wrapper (N x M board & vibrant colors)
"""

import importlib.util
import builtins
import tkinter as tk
from tkinter import simpledialog, messagebox

# Path to the user's original uploaded file
ORIGINAL_PATH = "2048_Game_Terminal-based.py"

# --- Import the user's module WITHOUT letting it auto-run the console game ---
_original_input = builtins.input
try:
    builtins.input = lambda *args, **kwargs: "NO"

    spec = importlib.util.spec_from_file_location("user_2048", ORIGINAL_PATH)
    user_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_mod)
finally:
    builtins.input = _original_input


class GUI2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 - GUI (Original Logic)")

        # --- Top controls frame ---
        controls = tk.Frame(root)
        controls.pack(padx=10, pady=8, anchor="n")

        self.rows_var = tk.IntVar(value=5)
        self.cols_var = tk.IntVar(value=5)

        tk.Label(controls, text="Rows:").grid(row=0, column=0)
        self.rows_entry = tk.Spinbox(controls, from_=5, to=15, width=5, textvariable=self.rows_var)
        self.rows_entry.grid(row=0, column=1, padx=(4,12))
        tk.Label(controls, text="Cols:").grid(row=0, column=2)
        self.cols_entry = tk.Spinbox(controls, from_=5, to=15, width=5, textvariable=self.cols_var)
        self.cols_entry.grid(row=0, column=3, padx=(4,12))

        new_btn = tk.Button(controls, text="New Game", command=self.new_game)
        new_btn.grid(row=0, column=4, padx=6)

        reset_btn = tk.Button(controls, text="Reset Board", command=self.reset_board_gui)
        reset_btn.grid(row=0, column=5, padx=6)

        # --- Score labels ---
        score_frame = tk.Frame(root)
        score_frame.pack(padx=10, pady=(0,8), anchor="n")
        self.score_label = tk.Label(score_frame, text="Score: 0", font=("Arial", 12, "bold"))
        self.score_label.pack(side="left", padx=8)
        self.high_label = tk.Label(score_frame, text="High: 0", font=("Arial", 12, "bold"))
        self.high_label.pack(side="left", padx=8)

        # --- Board frame ---
        self.board_frame = tk.Frame(root, bg="#bbada0")
        self.board_frame.pack(padx=12, pady=12, fill="both", expand=True)

        # store label widgets
        self.cell_labels = []

        # Bind keys
        root.bind("<Key>", self.on_key)
        root.bind('<Up>', lambda e: self.on_direction('W'))
        root.bind('<Down>', lambda e: self.on_direction('S'))
        root.bind('<Left>', lambda e: self.on_direction('A'))
        root.bind('<Right>', lambda e: self.on_direction('D'))

        # Initialize grid and start new game
        self.build_grid_from_user_board()
        self.new_game()

    # ------------------- GUI Build -------------------
    def build_grid_from_user_board(self):
        # remove old widgets
        for w in self.board_frame.winfo_children():
            w.destroy()
        self.cell_labels.clear()

        rows = len(user_mod.board)
        cols = len(user_mod.board[0])

        for r in range(rows):
            row_widgets = []
            for c in range(cols):
                lbl = tk.Label(self.board_frame, text="", width=6, height=3,
                               font=("Arial", 18, "bold"), bg="#cdc1b4",
                               fg="#776e65", relief="raised", bd=4)
                lbl.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
                row_widgets.append(lbl)
            self.cell_labels.append(row_widgets)

        # Make cells expand evenly
        for r in range(rows):
            self.board_frame.grid_rowconfigure(r, weight=1)
        for c in range(cols):
            self.board_frame.grid_columnconfigure(c, weight=1)

        self.update_gui()

    def update_gui(self):
        rows = len(user_mod.board)
        cols = len(user_mod.board[0])

        if rows != len(self.cell_labels) or cols != len(self.cell_labels[0]):
            self.build_grid_from_user_board()
            return

        for r in range(rows):
            for c in range(cols):
                val = user_mod.board[r][c]
                lbl = self.cell_labels[r][c]
                if val == " " or val == "":
                    lbl.config(text="", bg="#cdc1b4")
                else:
                    lbl.config(text=val, bg=self.color_for(int(val)))

        # Update scores
        try:
            self.score_label.config(text=f"Score: {user_mod.getCurrentScore()}")
            self.high_label.config(text=f"High: {user_mod.getHighScore()}")
        except Exception:
            pass

        self.root.update_idletasks()

    # ------------------- Tile Colors -------------------
    def color_for(self, value: int):
        if value == 2: return "#eee4da"
        if value == 4: return "#ede0c8"
        if value == 8: return "#f2b179"
        if value == 16: return "#f59563"
        if value == 32: return "#f67c5f"
        if value == 64: return "#f65e3b"
        if value == 128: return "#edcf72"
        if value == 256: return "#edcc61"
        if value == 512: return "#edc850"
        if value == 1024: return "#edc53f"
        if value == 2048: return "#edc22e"
        return "#3c3a32"  # fallback

    # ------------------- Key Handling -------------------
    def on_key(self, event):
        ch = event.char.upper() if hasattr(event, 'char') else ''
        if ch in ['W','A','S','D']:
            self.on_direction(ch)
        elif event.keysym in ['Up','Down','Left','Right']:
            pass
        elif ch == 'X':
            self.root.quit()

    def on_direction(self, key):
        try:
            possible = user_mod.checkMove(key)
        except Exception:
            possible = True

        if not possible:
            self.flash_message("Move not possible")
            return

        user_mod.playMove(key)
        try:
            user_mod.generateNumber()
            user_mod.setMaximumScore()
        except Exception:
            pass

        self.update_gui()

        # Check win
        try:
            if user_mod.is2048():
                if messagebox.askyesno("You reached 2048!","You made the 2048 tile. Continue playing?"):
                    pass
                else:
                    self.show_final_and_reset()
                    return
        except Exception:
            pass

        # Check if no moves left
        try:
            if not user_mod.shouldContinue():
                messagebox.showinfo("Game Over","No more valid moves! Game Over.")
                self.show_final_and_reset()
        except Exception:
            pass

    def flash_message(self, text):
        top = tk.Toplevel(self.root)
        top.overrideredirect(True)
        top.geometry('+%d+%d' % (self.root.winfo_rootx()+50, self.root.winfo_rooty()+50))
        tk.Label(top, text=text, bg='yellow').pack()
        self.root.after(600, top.destroy)

    # ------------------- Game Controls -------------------
    def new_game(self):
        rows = int(self.rows_var.get())
        cols = int(self.cols_var.get())

        # Ensure board is exactly rows x cols
        try:
            user_mod.createBoard(rows, cols)
        except Exception:
            user_mod.board = [[" " for _ in range(cols)] for _ in range(rows)]

        # Reset scores and board
        try:
            user_mod.resetScore()
        except Exception:
            pass
        try:
            user_mod.resetBoard()
        except Exception:
            for r in range(rows):
                for c in range(cols):
                    user_mod.board[r][c] = " "

        # Place two starting tiles
        try:
            user_mod.generateNumber()
            user_mod.generateNumber()
        except Exception:
            pass

        # Rebuild GUI
        self.build_grid_from_user_board()
        self.update_gui()

    def reset_board_gui(self):
        rows = int(self.rows_var.get())
        cols = int(self.cols_var.get())

        # Resize board to match current spinbox values
        try:
            user_mod.createBoard(rows, cols)
        except Exception:
            user_mod.board = [[" " for _ in range(cols)] for _ in range(rows)]

        # Reset scores
        try:
            user_mod.resetScore()
        except Exception:
            pass
        try:
            user_mod.resetBoard()
        except Exception:
            for r in range(rows):
                for c in range(cols):
                    user_mod.board[r][c] = " "

        # Place starting tiles
        try:
            user_mod.generateNumber()
            user_mod.generateNumber()
        except Exception:
            pass

        # Rebuild GUI to match new size
        self.build_grid_from_user_board()
        self.update_gui()


    def show_final_and_reset(self):
        try:
            user_mod.saveRoundStats()
        except Exception:
            pass

        try:
            final = f"Final High: {user_mod.getHighScore()}\nMax Tile: {user_mod.getMaxScore()}"
            messagebox.showinfo("Final Score", final)
        except Exception:
            pass

        self.new_game()


# ------------------- Run GUI -------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = GUI2048(root)
    root.mainloop()
