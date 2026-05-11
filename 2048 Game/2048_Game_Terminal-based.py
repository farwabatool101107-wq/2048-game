"""
    +--------------------------------------------------------------+
    |                                                              |
    |              2048 GAME APS PROJECT                           |
    |                                                              |
    |      Farwa -  fb11034                                        |
    |      Eshal -  ei11175                                        |
    |      Ayesha - ag11355                                        |
    |                                                              |
    +--------------------------------------------------------------+
"""


# ----------------------- Terminal Functions ----------------------- #
# Choose your operating system and UNCOMMENT only one block.

# =========================== WINDOWS ===========================
# import msvcrt
# import os
#
# def clearTerminal():
#     """Clears screen on Windows."""
#     os.system('cls')
#
# def getch():
#     """Reads a single key without Enter on Windows."""
#     return msvcrt.getch().decode('utf-8')


# ======================= LINUX / MAC ==========================
import sys, tty, termios
import os

def clearTerminal():
    """Clears screen on Linux/Mac."""
    os.system('clear')

def getch():
    """Reads a single key without Enter on Linux/Mac."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# -------------------------- Board & Game Stats --------------------------- #

# Initialize a 5x5 board with empty strings

board = [[" " for _ in range(5)] for _ in range(5)]

# Dictionary to store current score, high score, and round stats
gameStats = {
    "currentScore": 0,
    "highScore": 0,
    "rounds": []        # List of dicts for each round
}

# -------------------------- Board Setup & Display ------------------------ #

def setValues():
    """
    Set the board to predefined test values.
    Useful for debugging or testing specific scenarios.
    """
    global board
    board[:] = [ 
        ["2", "4", " ", "8", "128"],
        ["64", "4", "8", "512", "128"],
        [" ", "4", "16", "64", "128"],
        ["2", "4", "32", "2", "2"],
        ["16", "4", "32", "2", "2"]
    ]

def getBoard():
    """
    Prints the current state of the board in a formatted way.
    Adjusts spacing based on number length for alignment.
    """
    global board
    print("-" * (len(board[0]) * 12 + 1))
    for row in board:
        print("|", end="")
        for cell in row:
            length = len(cell)
            if length == 1:
                print(f"    {cell}      |", end="")
            elif length == 2:
                print(f"    {cell}     |", end="")
            elif length == 3:
                print(f"    {cell}    |", end="")
            elif length == 4:
                print(f"    {cell}   |", end="")
        print()  
        print("-" * (len(board[0]) * 12 + 1))

# ------------------------------ Move Functions --------------------------- #
#                               Move Right Functions
def shiftRightRow(row):
    """
    Shifts all non-empty tiles in a row to the right.
    Uses a while loop to push tiles until they reach the far right or another tile.
    """
    global board
    for index in range(len(board[row])-1,-1,-1):
        currentIndex = index
        while currentIndex < (len(board[row])-1) and board[row][currentIndex] != " " and board[row][currentIndex+1] == " ":
            board[row][currentIndex], board[row][currentIndex + 1] = board[row][currentIndex + 1], board[row][currentIndex]
            currentIndex+=1

def shiftBoardRight():
    """
    Shifts all rows in the board to the right.
    """
    global board
    for row in range (len(board)):
        shiftRightRow(row)

def mergeRightRow(row):
    """
    Merges adjacent equal tiles in a row from right to left.
    Updates score accordingly and clears the original tile after merging.
    """
    global board
    for index in range(len(board[row])-2,-1,-1):
        if board[row][index]!=" " and board[row][index] == board[row][index+1]:
            value = int(board[row][index])
            value*=2
            addPoints(value)
            board[row][index+1] = str(value)
            board[row][index] = " "

def mergeRightBoard():
    """
    Applies mergeRightRow to all rows in the board.
    """
    global board
    for row in range(len(board)):
        mergeRightRow(row)

def moveRight():
    """
    Performs a complete right move:
    1. Shift all tiles right.
    2. Merge equal tiles.
    3. Shift again to fill gaps after merging.
    """
    shiftBoardRight()
    mergeRightBoard()
    shiftBoardRight()

#                               Move Left Functions
def shiftLeftRow(row):
    """
    Shifts all non-empty tiles in a row to the left.
    Uses a while loop to push tiles until they reach the far left or another tile.
    """
    global board
    for index in range(1,len(board[row])):
        currentIndex = index
        while currentIndex > 0 and board[row][currentIndex] != " " and board[row][currentIndex - 1] == " ":
            board[row][currentIndex], board[row][currentIndex - 1] = board[row][currentIndex - 1], board[row][currentIndex]
            currentIndex-=1

def shiftBoardLeft():
    """
    Shifts all rows in the board to the left.
    """
    global board
    for row in range (len(board)):
        shiftLeftRow(row)

def mergeLeftRow(row):
    """
    Merges adjacent equal tiles in a row from left to right.
    Updates score accordingly and clears the original tile after merging.
    """
    global board
    for index in range(1,len(board[row])):
        if board[row][index]!=" " and board[row][index] == board[row][index-1]:
            value = int(board[row][index])
            value*=2
            addPoints(value)
            board[row][index-1] = str(value)
            board[row][index] = " "

def mergeLeftBoard():
    """
    Applies mergeLeftRow to all rows in the board.
    """
    global board
    for row in range(len(board)):
        mergeLeftRow(row)

def moveLeft():
    """
    Performs a complete left move:
    1. Shift all tiles left.
    2. Merge equal tiles.
    3. Shift again to fill gaps after merging.
    """
    shiftBoardLeft()
    mergeLeftBoard()
    shiftBoardLeft()
 
#                               Move Down Functions
def shiftDownCol(col):
    """
    Shifts all non-empty tiles in a column downward.
    Uses a while loop to push tiles until they reach the bottom or another tile.
    """
    global board
    for index in range(len(board)-1,-1,-1):
        currentIndex = index
        while currentIndex < (len(board)-1) and board[currentIndex][col] != " " and board[currentIndex+1][col] == " ":
            board[currentIndex][col], board[currentIndex + 1][col] = board[currentIndex + 1][col], board[currentIndex][col]
            currentIndex+=1

def shiftBoardDown():
    """
    Shifts all columns in the board downward.
    """
    global board
    for col in range (len(board[0])):
        shiftDownCol(col)

def mergeDownCol(col):
    """
    Merges adjacent equal tiles in a column from bottom to top.
    Updates score accordingly and clears the original tile after merging.
    """
    global board
    for index in range(len(board)-2,-1,-1):
        if board[index][col]!=" " and board[index][col] == board[index+1][col]:
            value = int(board[index][col])
            value*=2
            addPoints(value)
            board[index+1][col] = str(value)
            board[index][col] = " "

def mergeDownBoard():
    """
    Applies mergeDownCol to all columns in the board.
    """
    global board
    for col in range(len(board[0])):
        mergeDownCol(col)

def moveDown():
    """
    Performs a complete downward move:
    1. Shift all tiles down.
    2. Merge equal tiles.
    3. Shift again to fill gaps after merging.
    """
    shiftBoardDown()
    mergeDownBoard()
    shiftBoardDown()
 
#                               Move Up Functions
def shiftUpCol(col):
    """
    Shifts all non-empty tiles in a column upward.
    Uses a while loop to push tiles until they reach the top or another tile.
    """
    global board
    for index in range(1,len(board)):
        currentIndex = index
        while currentIndex > 0 and board[currentIndex][col] != " " and board[currentIndex-1][col] == " ":
            board[currentIndex][col], board[currentIndex - 1][col] = board[currentIndex - 1][col], board[currentIndex][col]
            currentIndex-=1

def shiftBoardUp():
    """
    Shifts all columns in the board upward.
    """
    global board
    for col in range (len(board[0])):
        shiftUpCol(col)

def mergeUpCol(col):
    """
    Merges adjacent equal tiles in a column from top to bottom.
    Updates score accordingly and clears the original tile after merging.
    """
    global board
    for index in range(1,len(board)):
        if board[index][col]!=" " and board[index][col] == board[index-1][col]:
            value = int(board[index][col])
            value*=2
            addPoints(value)
            board[index-1][col] = str(value)
            board[index][col] = " "

def mergeUpBoard():
    """
    Applies mergeUpCol to all columns in the board.
    """
    global board
    for col in range(len(board[0])):
        mergeUpCol(col)

def moveUp():
    """
    Performs a complete upward move:
    1. Shift all tiles up.
    2. Merge equal tiles.
    3. Shift again to fill gaps after merging.
    """
    shiftBoardUp()
    mergeUpBoard()
    shiftBoardUp()
 
# ------------------------------- Play Functions -------------------------- #
def playMove(key):
    """
    Executes the move corresponding to the key pressed by the player.
    Key mapping:
        W -> Up
        S -> Down
        A -> Left
        D -> Right
    """
    key = key.upper()
    if key == "W":
        moveUp()
    elif key == "S":
        moveDown()
    elif key == "A":
        moveLeft()
    elif key == "D":
        moveRight()

# ---------------------------- Game Continuation -------------------------- #

def checkMergeBoard():
    """
    Checks the entire board for any possible merges in any direction.
    Iterates through each tile and checks its adjacent tiles (up, down, left, right)
    for equality. Diagonal tiles are ignored. 
    Returns True if any merge is possible, otherwise False.
    """
    global board
    return checkHorizontalMerge() or checkVerticalMerge()


def checkHorizontalMerge():
    """
    Checks all rows in the board for possible horizontal merges.
    Calls checkRowMerge on each row. 
    Returns True if any horizontal merge is possible, otherwise False.
    """
    global board
    for row in range (len(board)):
        if checkRowMerge(row):
            return True
    return False

def checkRowMerge(row):
    """
    Checks a single row for adjacent tiles with the same value (left-right).
    Returns True if a merge is possible, otherwise False.
    """
    global board
    for col in range(1,len(board[row])):
        if board[row][col] == board[row][col-1]:
            return True 
    return False

def checkColMerge(col):
    """
    Checks a single column for adjacent tiles with the same value (top-bottom).
    Returns True if a merge is possible, otherwise False.
    """
    global board
    for row in range(1,len(board)):
        if board[row][col] == board[row-1][col]:
            return True 
    return False 

def checkVerticalMerge():
    """
    Checks all columns in the board for possible vertical merges.
    Calls checkColMerge on each column. 
    Returns True if any vertical merge is possible, otherwise False.
    """
    global board
    for col in range(len(board[0])):
        if checkColMerge(col):
            return True
    return False

def checkMove(key):
    """
    Determines if a move in the given direction is possible based on potential merges.
    Key mapping:
        W/S -> Up/Down: Check vertical merges
        A/D -> Left/Right: Check horizontal merges
    Returns True if a merge is possible in the given direction, otherwise False.
    """
    key = key.upper()
    if key == "W" or key == "S":
        return checkVerticalMerge()
    elif key == "A" or key == "D":
        return checkHorizontalMerge()
    else:
        return True
    
# ---------------------------- Board Functions ---------------------------- #
def resetBoard():
    """
    Resets the entire board by setting all tiles to empty (" ").
    """
    global board
    for row in range (len(board)):
        for col in range(len(board[row])):
            board[row][col] = " " 

def generateNumber():
    """
    Randomly generates a new tile number (2 or 4) and places it on the board.
    Calls placeNumber() to find a valid empty spot.
    """
    import random 
    opt_number = random.randint(1,2)
    number = 2 if opt_number == 1 else 4
    
    placeNumber(number)

def placeNumber(number):
    """
    Recursively places the given number on a random empty cell on the board.
    If the chosen cell is occupied, it retries until an empty cell is found.
    """
    global board
    import random
    row, col = random.randint(0, len(board)-1), random.randint(0, len(board[0])-1)
    if board[row][col] == " ":
        board[row][col] = str(number)
    else:
        placeNumber(number)

def is2048():
    """
    Checks if the board contains the 2048 tile.
    Returns True if found, otherwise False.
    """
    global board
    for row in range (len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "2048":
                return True 
    return False 

def getMaxScore():
    """
    Returns the current maximum tile value on the board.
    Ignores empty tiles.
    """
    global board
    return max(int(col) for row in board for col in row if col != " ")

def isFull():
    """
    Checks if the board is completely full (no empty cells).
    Returns True if full, otherwise False.
    """
    global board
    for row in range (len(board)):
        for col in range(len(board[row])):
            if board[row][col] == " ":
                return False 
    return True

def shouldContinue():
    """
    Determines if the game should continue.
    The game continues if the board is not full or if there is a possible merge.
    Returns True if the game can continue, otherwise False.
    """
    return (isFull() and checkMergeBoard()) or (not isFull())

def createBoard(row,col):
    """
    Creates a new board of given row x column size, initialized with empty tiles.
    """
    global board 
    board = [[" " for _ in range(col)] for _ in range(row)]

def resetGame():
    """
    Resets the board and score, then generates the first tile to start a new game.
    """
    resetBoard()
    resetScore()
    generateNumber()

def customizeBoard():
    """
    Allows the player to customize the board size.
    Prompts the player for confirmation, then validates row and column inputs.
    Defaults to 5x5 if player chooses not to customize.
    """

    print("Do you want to customize your board? ")
    message = validateMessage(input())
    
    if message.lower() == "yes":
        print("\n")
        print("Enter size of board : ")
        print()
        row = validateRow(int(input("Enter row: ")))
        col = validateColumn(int(input("Enter column: ")))
        createBoard(row,col)
    else:
        createBoard(5,5)

# ----------------------------- Validation Functions ---------------------- #
def validateKey(key):
    """
    Validates player input for movement keys.
    Acceptable inputs: W (up), A (left), S (down), D (right), X (exit).
    Prompts repeatedly until a valid key is entered.
    Returns the validated key.
    """
    while key.upper() not in ["W", "A", "S", "D", "X"]:
        print("Invalid Input:")
        prompt()
        key = getch()
    return key

def validateRestart(key):
    """
    Validates input for restarting or exiting the game.
    Acceptable inputs: R (restart), X (exit).
    Prompts repeatedly until a valid key is entered.
    Returns the validated key.
    """
    while key.upper() not in ["R", "X"]:
        print("Invalid Input:\nEnter 'R' to restart or 'X' to exit : ")
        key = getch()
    return key

def validateMessage(key):
    """
    Validates yes/no input messages from the player.
    Acceptable inputs: YES, NO (case-insensitive).
    Prompts repeatedly until a valid response is entered.
    Returns the validated message.
    """
    while key.upper() not in ["YES", "NO"]:
        print("Invalid Input:")
        key = input("Enter yes/no : ")
    return key

def validateContinuePlaying(cont):
    """
    Validates input for continuing or exiting after winning the game.
    Acceptable inputs: C (continue), X (exit).
    Prompts repeatedly until a valid response is entered.
    Returns the validated input.
    """
    while cont.upper() not in ["C", "X"]:
        print("Invalid Input:\nEnter 'X' to exit or 'C' to continue playing : ")
        cont = getch()
    return cont

def validateRow(row):
    """
    Validates row input for custom board size.
    Acceptable range: 5 to 15 inclusive.
    Prompts repeatedly until a valid number is entered.
    Returns the validated row number.
    """
    while row < 5 or row > 15:
        print("Invalid Input")
        row = int(input("Enter row in range (5 - 15):"))
    return row

def validateColumn(col):
    """
    Validates column input for custom board size.
    Acceptable range: 5 to 15 inclusive.
    Prompts repeatedly until a valid number is entered.
    Returns the validated column number.
    """
    while col < 5 or col > 15:
        print("Invalid Input")
        col = int(input("Enter column in range (5 - 15):"))
    return col

# ------------------------------ Messages -------------------------------- #
def prompt():
    print("Use W, A, S, D to move (W = up, A = left, S = down, D = right). Press X to exit.")

def displayIntro():
    print("+--------------------------------------------------+")
    print("|                                                  |")
    print("|               WELCOME TO 2048 GAME               |")
    print("|                                                  |")
    print("+--------------------------------------------------+\n")

    print("INTRODUCTION:")
    print("----------------------------------------------------")
    print("2048 is a single-player sliding puzzle game.")
    print("Your goal is to combine tiles with the same number")
    print("to reach the tile '2048' (or beyond, if you dare!).\n")

    print("You start with a 5x5 grid containing two random tiles (2 or 4).")
    print("Each move shifts all tiles in one direction.")
    print("When two tiles with the same number collide, they merge into one tile")
    print("with a value equal to their sum.\n")

    print("Example:")
    print("    2 + 2 -> 4")
    print("    4 + 4 -> 8")
    print("    8 + 8 -> 16")
    print("...and so on.\n")

    print("HOW TO PLAY:")
    print("----------------------------------------------------")
    print("Use the following keys to move tiles:")
    print("     W : Move UP")
    print("     S : Move DOWN")
    print("     A : Move LEFT")
    print("     D : Move RIGHT")
    print("     X : Exit Game\n")

    print("Each move adds a new tile (2 or 4) to the grid.")
    print("You can only move if at least one tile shifts or merges.")
    print("The game ends when:")
    print("     - The grid is full, AND")
    print("     - No more valid moves are possible.\n")

    print("WINNING CONDITION:")
    print("----------------------------------------------------")
    print("Combine tiles until you create the tile 2048!\n")

    print("TIPS:")
    print("----------------------------------------------------")
    print("1. Plan ahead — don't just move randomly.")
    print("2. Keep your largest tile in a corner.")
    print("3. Build values in descending order.")
    print("4. Avoid filling up the board too quickly!\n")

    print("+--------------------------------------------------+")
    print("|          PRESS ANY KEY TO START GAME!            |")
    print("+--------------------------------------------------+\n")

def displayWinMessage():
    print("+--------------------------------------------------+")
    print("|                                                  |")
    print("|                CONGRATULATIONS!                  |")
    print("|                                                  |")
    print("|               YOU HAVE WON THE GAME!             |")
    print("|                                                  |")
    print("+--------------------------------------------------+")
    print("|  You successfully created the 2048 tile!         |")
    print("|  But you can keep playing to reach higher tiles. |")
    print("|                                                  |")
    print("|  Press 'C' to Continue playing, or 'X' to Exit.  |")
    print("+--------------------------------------------------+\n")

def displayGoodbyeMessage():
    print("+--------------------------------------------------+")
    print("|                                                  |")
    print("|          CONGRATULATIONS! YOU WON!               |")
    print("|                                                  |")
    print("+--------------------------------------------------+")
    print("|  You've already conquered the 2048 tile!         |")
    print("|  True mastery lies in pushing beyond limits.     |")
    print("|                                                  |")
    print("|  See you next time, champion!                    |")
    print("|  Press 'R' to Restart or 'X' to Exit the game.  |")
    print("+--------------------------------------------------+\n")

def displayLoseMessage():
    print("+--------------------------------------------------+")
    print("|                                                  |")
    print("|                    GAME OVER!                    |")
    print("|                                                  |")
    print("+--------------------------------------------------+")
    print("|  No more valid moves are possible.               |")
    print("|  The board is full, and you cannot continue.     |")
    print("|                                                  |")
    print("|  Better luck next time!                          |")
    print("|  Press 'R' to Restart or 'X' to Exit the game.   |")
    print("+--------------------------------------------------+\n")

def displayExitMessage():
    print("+--------------------------------------------------+")
    print("|                                                  |")
    print("|               SEE YOU NEXT TIME!                 |")
    print("|                                                  |")
    print("+--------------------------------------------------+")
    print("|  You exited the game before finishing.           |")
    print("|  Maybe next time you'll reach 2048!              |")
    print("|                                                  |")
    print("|  Press 'R' to Restart or 'X' to Exit fully.      |")
    print("+--------------------------------------------------+")

# ----------------------------- Score Functions --------------------------- #
def addPoints(points):
    """
    Adds points to the current score and updates the high score if necessary.
    Called whenever tiles are merged to increase the player's score.
    """
    global gameStats
    gameStats["currentScore"] += points
    gameStats["highScore"] = max(gameStats["highScore"], gameStats["currentScore"])

def getCurrentScore():
    """
    Returns the current score of the ongoing round.
    """
    global gameStats
    return gameStats["currentScore"]

def getHighScore():
    """
    Returns the current high score across all rounds played.
    """
    global gameStats
    return gameStats["highScore"]

def resetScore():
    """
    Resets the current score to 0.
    Typically used when starting a new game or round.
    """
    global gameStats
    gameStats["currentScore"] = 0

def saveRoundStats():
    """
    Saves statistics of the current round into the gameStats dictionary.
    Stores maximum tile, high score, and current score for the round.
    """
    global gameStats
    gameStats["rounds"].append({
        "roundMaxScore": getMaxScore(),
        "roundHighScore": getHighScore(),
        "roundCurrentScore": getCurrentScore()
    })

def setMaximumScore():
    """
    Updates the maximum score of the current round in the gameStats dictionary.
    """
    global gameStats
    gameStats["roundMaxScoreCurrent"] = getMaxScore()

# def getFinalHighScore():
#     """
#     Returns the highest score achieved across all rounds.
#     Useful for end-of-game summary.
#     """
#     global gameStats
#     return max(roundStat["roundHighScore"] for roundStat in gameStats["rounds"])

# def getFinalMaximumScore():
#     """
#     Returns the maximum tile value achieved across all rounds.
#     Useful for end-of-game summary.
#     """
#     global gameStats
#     return max(roundStat["roundMaxScore"] for roundStat in gameStats["rounds"])

def scoreBoard():
    """
    Returns a formatted string showing the current score and high score.
    Useful for displaying during gameplay.
    """
    global gameStats
    return f"Score: {gameStats['currentScore']} | High Score: {gameStats['highScore']}"

def displayFinalScoreBoard():
    """
    Displays a detailed summary of all rounds played and their statistics.
    Includes per-round maximum score, high score, current score,
    as well as overall maximum and highest scores.
    """
    global gameStats
    box_width = 48
    inner = box_width - 2

    print()
    print("+" + "-" * (box_width - 2) + "+")
    print("|" + f"{'2048 GAME SUMMARY':^{inner}}" + "|")
    print("+" + "-" * (box_width - 2) + "+")
    print()

    overallHigh = 0
    overallMax = 0
    roundNumber = 1  
    
    for roundStats in gameStats["rounds"]:
        print("+" + "-" * (box_width - 2) + "+")
        print("|" + f"{' ROUND ' + str(roundNumber) + ' ':^{inner}}" + "|")
        print("+" + "-" * (box_width - 2) + "+")

        for key, value in roundStats.items(): 
            keyName = key.replace("_", " ").title()
            print("|" + f"{keyName:<20}: {value:<25}" + "|")

        print("+" + "-" * (box_width - 2) + "+")
        print()

        overallHigh = max(overallHigh, roundStats["roundHighScore"])
        overallMax = max(overallMax, roundStats["roundMaxScore"])

        roundNumber += 1 

    print("+" + "-" * (box_width - 2) + "+")
    print("|" + f"{' FINAL RESULT ':^{inner}}" + "|")
    print("+" + "-" * (box_width - 2) + "+")
    print("|" + f"{'Final High Score : ' + str(overallHigh):<{inner}}" + "|")
    print("|" + f"{'Max Score Overall : ' + str(overallMax):<{inner}}" + "|")
    print("+" + "-" * (box_width - 2) + "+")
    print()
    print(f"{'Thanks for playing!':^{box_width}}")
    print()


# ---------------------------- Play Game Logic --------------------------- #
def startGame():
    """
    Main function to handle the entire flow of a 2048 game session.
    Handles introduction, board setup, game loop, player moves,
    win/loss conditions, round stats, and final score display.
    """
    # Display the game introduction and instructions
    displayIntro()
    getch()     # Wait for player to press a key before starting

    cont = "R"   # Initialize continuation variable for restarting rounds

    clearTerminal()

    while cont.upper() == "R":

        print()
        customizeBoard()    # Ask player if they want to customize board size
        clearTerminal()
        
        resetGame()     # Reset board and scores, and place initial random number

        key = ""   # Variable to store player's input for moves
        showOnce,win = False,False      # Flags for displaying win message once

        # Inner loop: runs while the game can continue and player hasn't exited
        while shouldContinue() and key.upper() != "X":

            generateNumber()     # Add a new random tile (2 or 4) after every move
            print("\n| Game_2048   | Maximum Score: ",getMaxScore()," | ",scoreBoard())
            getBoard()      # Display the current board state

            prompt()    # Show movement instructions
            key = validateKey(getch())      # Validate player's move input
            print()

            # Check if board is full and no move is possible; break if true
            if isFull() and not checkMove(key):     
                break

            playMove(key)       # Execute the player's move (up/down/left/right)
            setMaximumScore()   # Update the maximum tile value after move

            # Check for 2048 tile and display win message only once
            if not showOnce and is2048():
                win = True 
                displayWinMessage()
                key = validateContinuePlaying(getch())     # Ask player to continue or exit
                showOnce = True
            
            clearTerminal()

        saveRoundStats()        # Save the statistics of the completed round
        
        # After the inner loop ends, determine final message and continuation
        if win:
            displayGoodbyeMessage()     # Show congratulations if player reached 2048
        else:
            if isFull():
                displayLoseMessage()    # Show game over if no moves possible
            else:
                displayExitMessage()    # Show exit message if player quits manually
        cont = validateRestart(getch())      # Ask player to restart or exit
        
        clearTerminal()

    # After all rounds are finished, display summary of all rounds
    displayFinalScoreBoard()

# ------------------------ Game Entry Point ----------------------------- #
def playGame():
    """
    Entry point for the 2048 game.
    Asks the player if they want to start a game.
    If the player agrees, the main game loop (startGame) begins.
    Otherwise, prints a goodbye message and exits.
    """

    clearTerminal()
    print("Do you want to play a 2048 game ? ")
    message = validateMessage(input())

    if message.upper() == "YES":
        clearTerminal()
        startGame()
    else:
        print("Good Bye!! ")

#                           Start the game
playGame()
print(gameStats)