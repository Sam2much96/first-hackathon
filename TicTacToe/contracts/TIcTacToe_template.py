#!/usr/bin/env python3
#TIC TAC TOE game

"""


"""

# *************************************************
# Simple Tic Tac Toe game by INhumanity_Studios
# Released under MIT License
# *************************************************
# Simple Tic Tac Toe game
# 
# Features:
# Contains Randomized CPU player 
# 

import random



def print_board(board):
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

def get_cpu_move(board):

        # Adding CPU AI

        print ("debug: ",board)
        move = random.randint(0, 8)

        return move



def tictactoe():
    GameRound = 0
    board = [' '] * 9
    player = 'X'
    print("Welcome to Tic Tac Toe!")
    print_board(board)
 

    running_game_loop = True

    while running_game_loop:
        if player == "X":
            move = get_player_move()#input("Enter a position from 1-9 (player " + player + "): ")
        elif player == "O":
            move = get_cpu_move(board)

        try:
   
            if board[move] != ' ':
                print("That space is already taken, please choose another.")
           
                continue
           
            board[move] = player
            print_board(board)
            print ("GameRound: ", GameRound)
            


            # End Loop
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
    tictactoe()