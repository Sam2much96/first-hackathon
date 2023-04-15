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
        stack_type = TealType.uint64

        )



tictactoe = Application(
    "TicTacToe",
    descr = " TicTacToe game. A Scratch variable for the Game State using Box storage",
    state =GameState()

    )

does_nothing = Int (0)

@tictactoe.external
def register_player() -> Expr:
    
    # Save Game Round
    return tictactoe.state.GameRound.set(Int(0))



# Game Logic
@tictactoe.external
def get_player_move(move : abi.Uint64)-> Expr:         
     
    return Seq(

        If (tictactoe.state.GameRound.get() == Int(0))
        .Then(tictactoe.state.boxA[Txn.sender()].set(move))
        )


@tictactoe.external
def get_cpu_move(move : abi.Uint64)-> Expr:
    # Generate Random Move

    move.set(random.randrange(9))
    # Implement Game ROund 
    return tictactoe.state.boxA[Txn.sender()].set(move)



#@Subroutine(TealType.uint64)
#@tictactoe.external


#Compares the box bytes to determine a winner


def check_win(
    init: Expr = Int(0),
    delete: Expr = Int(0),
    update: Expr = Int(0),
    opt_in: Expr = Int(0),
    close_out: Expr = Int(0),
    no_op: Expr = Int(0),

    )-> Expr:
    return Cond (
        #[boxA.get() == player and boxB.get() == player and boxC.get() == player.get()]

         [tictactoe.state.boxA[Txn.sender()].get() == Bytes("")], no_op,

         [tictactoe.state.boxA[Txn.sender()].get() == Bytes("")], no_op

         )
                  

        #(board[3] == player and board[4] == player and board[5] == player) or
    #    (board[6] == player and board[7] == player and board[8] == player) or
    #    (board[0] == player and board[3] == player and board[6] == player) or
    #    (board[1] == player and board[4] == player and board[7] == player) or
    #    (board[2] == player and board[5] == player and board[8] == player) or
    #    (board[0] == player and board[4] == player and board[8] == player) or
    #    (board[2] == player and board[4] == player and board[6] == player)):
    
    # Get Game State From Box
    #if state.get() == player.get(): #Bytes("X"):

    #return player.get()
    #else:
    #    return player.set(Bytes("False"))



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

    # Create Algod Node



    GameRound = 0
    board = [' '] * 9
    player = 'X'
    print("Welcome to Tic Tac Toe!")
    print_board(board)
 

    running_game_loop = True

    while running_game_loop:
        if player == "X":
            move = input("Enter a position from 1-9 (player " + player + "): ")

            # Send Application Call Via SmartContract

        elif player == "O":

            # Get CPU move from Application Call

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
