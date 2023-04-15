from pyteal import *


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
    board = BoxMapping(abi.Uint64, abi.Uint64) #TealType.uint64 #BoxMapping(TealType.uint64, TealType.uint64) 
     

        

tictactoe = Application(
    "TicTacToe",
    descr = " TicTacToe game. A Scratch variable for the Game State using Box storage",
    state =GameState()

    )



@tictactoe.external
def register_player_value(value: abi.Uint64) -> Expr:
    
    # Save to box Storage
    # access an element in the mapping by key
    return tictactoe.state.board[Txn.sender()].set(value)



# Game Logic
@tictactoe.external
def get_player_move(move : abi.Uint64)-> Expr:         
     
    return tictactoe.state.board[Txn.sender()].set(move)


@tictactoe.external
def get_cpu_move(move : abi.Uint64)-> Expr:
    move.set(random.randrange(9)) # Generate Random Move
    return tictactoe.state.board[Txn.sender()].set(move)



@Subroutine(TealType.uint64)
def check_win(board : abi.Byte, player : abi.Byte)-> Expr:
    #if ((board[0] == player and board[1] == player and board[2] == player) or
    #    (board[3] == player and board[4] == player and board[5] == player) or
    #    (board[6] == player and board[7] == player and board[8] == player) or
    #    (board[0] == player and board[3] == player and board[6] == player) or
    #    (board[1] == player and board[4] == player and board[7] == player) or
    #    (board[2] == player and board[5] == player and board[8] == player) or
    #    (board[0] == player and board[4] == player and board[8] == player) or
    #    (board[2] == player and board[4] == player and board[6] == player)):
    
    # Get Game State From Box
    if state.get() == player.get(): #Bytes("X"):

        return player.get()
    else:
        return player.set(Bytes("False"))



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



# Runs the Game Client for better Player UX

def tictactoe_client() -> None:
    GameRound = 0
    board = [' '] * 9
    player = 'X'
    print("Welcome to Tic Tac Toe!")
    print_board(board)
 

    running_game_loop = True

    while running_game_loop:
        if player == "X":
            move = input("Enter a position from 1-9 (player " + player + "): ")
        elif player == "O":
            move = get_cpu_move(board)

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

    calc_app_spec = tictactoe.build()
    print(calc_app_spec.approval_program)
    print(calc_app_spec.clear_program)
    print(calc_app_spec.to_json())

 


    """
    Write Out the Approval and Clear Programs. 
    Dump the Contract's method to a .json file.

    """

    with open("approval_program.teal", "w") as f:
        f.write(calc_app_spec.approval_program)

    with open("clear_state_program.teal", "w") as f:
        f.write(calc_app_spec.clear_program)
        
    with open("TicTacToe.json", "w") as f:
        f.write(json.dumps(calc_app_spec.to_json(), indent=4))

    tictactoe_client()
