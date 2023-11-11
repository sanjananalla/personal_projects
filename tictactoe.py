# this project will generate a tic tac toe game within the python console
import random

# initializing the game board
gameBoard: list[str] = ["_", "_", "_",
                        "_", "_", "_",
                        "_", "_", "_"]

# more global variables
currentPlayer: str = "A"
winner: bool = None
playingGame: bool = True

def createBoard(gameBoard):
    print(gameBoard[0] + " " + gameBoard[1] + " " + gameBoard[2])
    print("")
    print(gameBoard[3] + " " + gameBoard[4] + " " + gameBoard[5])
    print("")
    print(gameBoard[6] + " " + gameBoard[7] + " " + gameBoard[8])

# user input
def userInput(gameBoard):
    inputNum = int(input ("Enter a number between 1 and 9: "))
    if inputNum >= 1 and inputNum <= 9 and gameBoard[inputNum-1] == "_":
        gameBoard[inputNum-1] = currentPlayer
    else:
        print("This spot is already occupied.")
# checking rows/horizontal
def checkRow(gameboard):
    global winner
    if ((gameBoard[0] == gameBoard[1] == gameBoard[2]) and (gameBoard[1] != "_")):
        winner = gameBoard[0]
        return True
    elif ((gameBoard[3] == gameBoard[4] == gameBoard[5]) and (gameBoard[3] !="_")):
        winner = gameBoard[3]
        return True
    elif ((gameBoard[6] == gameBoard[7] == gameBoard[8]) and (gameBoard[8] != "_")):
        winner = gameBoard[6]
        return True

# checking columns/vertical
def checkColumn(gameBoard):
    global winner
    if ((gameBoard[0] == gameBoard[3] == gameBoard[6]) and (gameBoard[0] != "_")):
        winner = gameBoard[0]
        return True
    elif ((gameBoard[1] == gameBoard[4] == gameBoard[7]) and (gameBoard[1] != "_")):
        winner = gameBoard[1]
        return True
    elif ((gameBoard[2] == gameBoard[5] == gameBoard[8]) and (gameBoard[2] != "_")):
        winner = gameBoard[2]
        return True

# checking diagonals
def checkDiagonal(gameBoard):
    global winner
    if ((gameBoard[0] == gameBoard[4] == gameBoard[8]) and (gameBoard[0] != "_")):
        winner = gameBoard[0]
        return True
    elif ((gameBoard[2] == gameBoard[4] == gameBoard[6]) and (gameBoard[2] != "_")):
        winner = gameBoard[2]
        return True

# checking for a tie
def checkTie(gameBoard):
    return "_" not in gameBoard
        
# checking for a winner
def checkWin():
    return (checkDiagonal(gameBoard) or checkRow(gameBoard) or checkColumn(gameBoard))

# switch to next player
def switchUser(gameBoard):
    global currentPlayer
    if currentPlayer == "A":
        currentPlayer = "B"
    else:
        currentPlayer = "A"

# creating a computer player
def computer(gameBoard):
    while currentPlayer == "B":
        position = random.randint(0, 8)
        if gameBoard[position] == "_":
            gameBoard[position] = "B"
            switchUser(gameBoard)

# running everything
while playingGame:
    createBoard(gameBoard)
    userInput(gameBoard)
    if checkWin():
        createBoard(gameBoard)
        print(f"The winner is {winner}!")
        break
    if checkTie(gameBoard):
        createBoard(gameBoard)
        print("It is a tie!")
        break
    switchUser(gameBoard)
    computer(gameBoard)
   
