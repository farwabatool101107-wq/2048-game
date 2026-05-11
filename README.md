# 2048-game
2048 puzzle game in Python with dual-mode support — terminal (console) and Tkinter GUI. Features customizable N×M board size, real-time score tracking, WASD + arrow key controls, win/game-over detection, and a clean color-coded tile interface.
# 2048 Game

2048 Game is a Python implementation of the classic 2048 puzzle game developed as an APS course project. The project supports two modes of play: a terminal-based console interface and a graphical GUI built with Tkinter, both powered by the same core game engine.

The system handles board initialization, tile shifting and merging in all four directions, random tile generation, score tracking, and win/loss detection. The GUI wraps the terminal module at runtime using importlib, keeping the logic layer fully separate from the presentation layer.

---

# Features

- Terminal-based gameplay with ASCII board rendering
- Tkinter GUI with color-coded tiles
- Configurable N x M board size (5x5 up to 15x15)
- Single-keypress input without requiring Enter (Linux/macOS)
- WASD and arrow key support
- Real-time score and high score tracking
- Win detection when the 2048 tile is reached
- Game Over detection when no valid moves remain
- Restart or exit after each round
- Per-round stats saved and displayed in a final summary

---

# Implemented Algorithms and Techniques

## Move Logic
- Tile shifting in all four directions (up, down, left, right)
- Tile merging with equal-value collision detection
- Three-step move execution: shift, merge, shift

## Board Management
- Dynamic N x M board creation
- Random tile placement (value 2 or 4) on empty cells
- Full board detection
- Move validity checking before execution

## Scoring
- Points added on every merge equal to the resulting tile value
- High score updated continuously across moves
- Maximum tile value tracked per round
- Round statistics saved for end-of-session summary

---

# Workflow

1. Player launches terminal or GUI mode
2. Board size is configured (default 5x5, customizable)
3. Two tiles are placed randomly to start the game
4. Player inputs a direction (W/A/S/D or arrow keys)
5. Tiles shift and merge in the chosen direction
6. A new tile is generated after each valid move
7. Score updates on every merge
8. Win condition checked for 2048 tile
9. Game Over triggered when board is full and no moves remain
10. Round stats saved and final summary displayed

---

# Project Structure

```text
2048-game/
│
├── 2048_Game_Terminal-based.py   # Core game logic and terminal interface
├── 2048_Game_GUI.py              # Tkinter GUI wrapper
└── README.md
```

---

# Controls

| Key       | Action      |
|-----------|-------------|
| W / Up    | Move Up     |
| S / Down  | Move Down   |
| A / Left  | Move Left   |
| D / Right | Move Right  |
| R         | Restart     |
| X         | Quit / Exit |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/farwabatool101107-wq/2048-game.git
cd 2048-game
```

## Run Terminal Mode

```bash
python 2048_Game_Terminal-based.py
```

Note: Terminal mode uses tty and termios and runs on Linux and macOS.
For Windows, uncomment the msvcrt block inside the file and comment out the Linux block.

## Run GUI Mode

```bash
python 2048_Game_GUI.py
```

Both files must be in the same directory.

---

# Technologies Used

- Python 3
- Tkinter
- tty / termios (Linux/macOS single-keypress input)
- msvcrt (Windows single-keypress input)
- importlib

---

# Team

- Farwa Batool
- Eshal Imran
- Ayesha Ghazi
