from pyteal import *
from pyteal.ast import *

from beaker import Application, sandbox, GlobalStateValue
from beaker.client import ApplicationClient

from beaker.lib.storage import BoxMapping
import json


# Game Required Imports
import random
import math


class GameState:
    # Docs : https://algorand-devrel.github.io/beaker/html/boxes.html
    # For Player MOVES

    # Use 9 Boxes with "" bytes for storing Board Placements

    boxA = BoxMapping(abi.Byte, abi.Uint64) #TealType.uint64 #BoxMapping(TealType.uint64, TealType.uint64) 
     
    boxB = BoxMapping(abi.Uint64, abi.Uint64)

    boxC = BoxMapping(abi.Uint64, abi.Uint64)
    boxD = BoxMapping(abi.Uint64, abi.Uint64)
    boxE = BoxMapping(abi.Uint64, abi.Uint64)
    boxF = BoxMapping(abi.Uint64, abi.Uint64)
    boxG = BoxMapping(abi.Uint64, abi.Uint64)
    boxH = BoxMapping(abi.Uint64, abi.Uint64)
    boxI = BoxMapping(abi.Uint64, abi.Uint64)
        
    # Declare a Global Winner
    winner = GlobalStateValue(
        stack_type = TealType.uint64

        )

    # Global Game Round
    GameRound = GlobalStateValue(
        stack_type = TealType.uint64,
        descr = " Stores the Game Round of A current runing Game"
        )


   # Global Game State
    StoredGameState = GlobalStateValue(
        stack_type = TealType.uint64,
        descr = " Stores the Game State which could either be playing, player_won, bad_move "
        )

    # Current Game State stored to a scratch var
    GameState = ScratchVar(TealType.uint64)


tictactoe = Application(
    "TicTacToe",
    descr = " TicTacToe game. A Scratch variable for the Game State using Box storage",
    state =GameState()

    )



@tictactoe.external
def register_player() -> Expr:
    
    # Save Game Round
    return tictactoe.state.GameRound.set(Int(0))



# Game Logic
@tictactoe.external
def get_player_move(move : abi.Uint64)-> Expr:         
     
    return Seq(
    
        If (tictactoe.state.StoredGameState.get() == Int(0)) # if game playing
        .Then(tictactoe.state.boxA[Txn.sender()].set(move)) # Save first move
        )

@tictactoe.external
def get_cpu_move(move : abi.Uint64)-> Expr:
    # Generate Random Move

    move.set(random.randrange(9))
    # Implement Game ROund 
    return tictactoe.state.boxA[Txn.sender()].set(move)



#@Subroutine(TealType.uint64)


#Compares the box bytes to determine a winner




#         [tictactoe.state.boxA[Txn.sender()].get() == Bytes("")], no_op,

#         [tictactoe.state.boxB[Txn.sender()].get() == Bytes("")], no_op



"""

@tictactoe.external
def add(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> Expr:
    #Add a and b, return the result
    return output.set(a.get() + b.get())


@tictactoe.external
def mul(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> Expr:
    #Multiply a and b, return the result
    return output.set(a.get() * b.get())


@tictactoe.external
def sub(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> Expr:
    #Subtract b from a, return the result
    return output.set(a.get() - b.get())


@tictactoe.external
def div(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> Expr:
    #Divide a by b, return the result
    return output.set(a.get() / b.get())













def minimax(board, depth, is_maximizing)-> Expr:
        if check_win(board, 'O'):
            return 1
        elif check_win(board, 'X'):
            return -1
        elif ' ' not in board:
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = minimax(board, depth+1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = minimax(board, depth+1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

"""


# Client Side Code

def print_board(board) :
    print("   |   |")
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("   |   |")
    print("-----------")
    print("   |   |")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("   |   |")
    print("-----------")
    print("   |   |")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print("   |   |")


def check_win(board, player):
    synchronize_game_state(board)
    if ((board[0] == player and board[1] == player and board[2] == player) or
        (board[3] == player and board[4] == player and board[5] == player) or
        (board[6] == player and board[7] == player and board[8] == player) or
        (board[0] == player and board[3] == player and board[6] == player) or
        (board[1] == player and board[4] == player and board[7] == player) or
        (board[2] == player and board[5] == player and board[8] == player) or
        (board[0] == player and board[4] == player and board[8] == player) or
        (board[2] == player and board[4] == player and board[6] == player)):
        return True
    else:
        return False


def synchronize_game_state(board)-> None:
    # Synchronize client board state with App State
    pass


    # Mini Max AI Algorithm for CPU
def minimax(board, depth, is_maximizing):
        if check_win(board, 'O'):
            return 1
        elif check_win(board, 'X'):
            return -1
        elif ' ' not in board:
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = minimax(board, depth+1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = minimax(board, depth+1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score


def generate_cpu_best_move(board):


    
    # Main function
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move




def get_player_move():

        move = input("Enter a number between 1-9 to place your mark: ")
        try:
            move = int(move) - 1
            if move >= 0 and move < 9 : #and board[move] == 0:
                return move
            else:
                print("Invalid move. Try again.please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Try again.")


# Runs the Game Client for better Player UX

def tictactoe_client() -> None:

    # Create Algod Node



    GameRound = 0
    board : List[str] = [' '] * 9
    player = 'X'
    print("Welcome to Tic Tac Toe!")
    print_board(board)
 

    running_game_loop = True

    while running_game_loop:
        if player == "X":
            move = get_player_move()
        elif player == "O":

            # Get CPU move from Application Call

            move = generate_cpu_best_move(board)

        try:
   
            # Register these game state to Scratch State Value
            if board[move] != ' ':
                # bad move
                print("That space is already taken, please choose another.")
           
                continue
           

            # playing
            board[move] = player
            print_board(board)
            print ("GameRound: ", GameRound)
            


            # End Loop
            # player won
            if check_win(board, player):
                print("Congratulations, player " + player + " wins!")
                break
            if ' ' not in board:
                print("It's a tie!")
                break
            


            # Alternate Players
            if player == 'X':
                player = 'O'
                GameRound += 1

            else:
                player = 'X'
        except ValueError:
            print("Invalid move, please enter a number between 1 and 9.")
            continue



if __name__ == "__main__":

    """
    Write Out the Approval and Clear Programs. 
    Dump the Contract's method to a .json file.

    """
    tictactoe_app = tictactoe.build()
    print(tictactoe_app.approval_program)
    
    #print(tictactoe_app.clear_program)
    #print(tictactoe_app.to_json())

 

    with open("approval_program.teal", "w") as f:
        f.write(tictactoe_app.approval_program)

    #with open("clear_state_program.teal", "w") as f:
    #    f.write(calc_app_spec.clear_program)
        
    #with open("TicTacToe.json", "w") as f:
    #    f.write(json.dumps(calc_app_spec.to_json(), indent=4))

    """
    Run Game Loop

    """
    tictactoe_client()
