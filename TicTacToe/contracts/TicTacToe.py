from pyteal import *
from pyteal.ast import *

from beaker import Application, sandbox, GlobalStateValue, BuildOptions
from beaker.client import ApplicationClient

from beaker.lib.storage import BoxMapping
import json


# Game Required Imports
import random
import math




# Algod Client Required Imports
from algosdk.v2client import algod
from algosdk import account
from algosdk import mnemonic
from algosdk.abi import Contract, Method, Returns, Argument

from algosdk.abi import ByteType

#from algosdk import logic

from algosdk import transaction
from algosdk.transaction import StateSchema 

#import algosdk.atomic_transaction_composer 
from algosdk.atomic_transaction_composer import AccountTransactionSigner, AtomicTransactionComposer

import base64



# Smart Cntract

class GameState:
    # Docs : https://algorand-devrel.github.io/beaker/html/boxes.html
    # For Player MOVES

    # Use 9 Boxes with "" bytes for storing Board Placements

    #board = BoxMapping(abi.Address, abi.Uint64) #TealType.uint64 #BoxMapping(TealType.uint64, TealType.uint64) 
     

        # Declare a Global Winner
    board = GlobalStateValue(
        stack_type = TealType.uint64

    )   
    
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
        stack_type = TealType.bytes,
        descr = " Stores the Game State which could either be playing, player_won, bad_move "
        )

    # Current Game State stored to a scratch var
    GameState = ScratchVar(TealType.bytes)


tictactoe = Application(
    "TicTacToe",
    descr = " A TicTacToe game with CPU best-move AI",
    state =GameState(),
    build_options=BuildOptions(
            avm_version=8, scratch_slots=True, frame_pointers=True, 
        )

    )




#def __init__():


@tictactoe.external
def register_player() -> Expr:
    
    # Save Game Round
    return tictactoe.state.GameRound.set(Int(0))



# Game Logic
@tictactoe.external
def synchronize_game(board : abi.Uint64, game_state: abi.Uint64)-> Expr:         
    #return tictactoe.state.board[Txn.sender()].set(board) # for box storage
    return Seq(
        tictactoe.state.board.set(board.get()),

        If(game_state.get() == Int (0))
         .Then(tictactoe.state.GameState.store(Bytes("playing")))
         .ElseIf(game_state.get() == Int (1))
         .Then(tictactoe.state.GameState.store(Bytes("bad move")))
         .ElseIf(game_state.get() == Int (2))
         .Then(tictactoe.state.GameState.store(Bytes("player won")))

        )



"""

# Client Side Code

"""



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


    print ("CPU Playing ...")
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

    board_as_int = best_move
    return best_move




def get_player_move():

        move = input("Enter a number between 1-9 to place your mark: ")
        try:
            move = int(move) - 1
            if move >= 0 and move < 9 : #and board[move] == 0:
                #board_as_int = move
                return move
            else:
                print("Invalid move. Try again.please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Try again.")




# Runs the Game Client for better Player UX

def tictactoe_client(board : list[str]) -> None:

    board_as_int = 0
    GameRound = 0
    
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
                synchronize_game_state(algod_client, app_id, board_as_int, 1) # bad move
                continue
           

            # playing
            board[move] = player
            print_board(board)
            board_as_int = boardToint(board)
            print ("Board as Int: ", board_as_int)


            synchronize_game_state(algod_client, app_id, board_as_int, 0) #playing
            print ("GameRound: ", GameRound)
            


            # End Loop
            # player won
            if check_win(board, player):
                print("Congratulations, player " + player + " wins!")
                synchronize_game_state(algod_client, app_id, board_as_int, 2) # player won
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



# Utility Methods


def deploy(_params, mnemonic_ ,algod_client, fee, global_ints : int , global_bytes : int):

    _params.flat_fee = True
    _params.fee = fee


    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    #global_ints = 0
    #global_bytes = 0
    global_schema = StateSchema(global_ints, global_bytes)
    local_schema = StateSchema(local_ints, local_bytes)



    response = algod_client.compile(tictactoe_app.approval_program)
    print ("Raw Response =",response )
    print("Response Result = ",response['result'])
    print("Response Hash = ",response['hash'])


    # compile program to binary
    approval_program_compiled = compile_program(algod_client, tictactoe_app.approval_program)

    # compile program to binary
    clear_state_program_compiled = compile_program(algod_client, tictactoe_app.clear_program)



    app_id = create_app(algod_client,_params ,mnemonic_, approval_program_compiled, clear_state_program_compiled, global_schema, local_schema)

    # Create the applicatiion on chain, set the app id for the app client & store app secret
    print(f"Created App with id: {app_id} ")






# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])





# create new application
def create_app(client, params, private_key, approval_program, clear_program, global_schema, local_schema):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    #print (sender)

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    #params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(sender, params, on_complete, \
                                            approval_program, clear_program, \
                                            global_schema, local_schema)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # wait for confirmation
    try:
        transaction_response = transaction.wait_for_confirmation(client, tx_id, 4)
        print("TXID: ", tx_id)
        print("Result confirmed in round: {}".format(transaction_response['confirmed-round']))

    except Exception as err:
        print(err)
        return

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id:", app_id)

    return app_id





# delete application
def delete_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    #params.flat_fee = True
    #params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(
        sender= sender, 
        sp= params, 
        index= index,
        
        #Disabling boxes until implementation in Algonaut
        #boxes=[[0, "BoxA"],[0, "BoxB"],[0, "BoxC"], [0,""],[0,""],[0,""]],
        )

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Deleted app-id:", transaction_response["txn"]["txn"]["apid"])






# Uses Atomic Transaction Composer to Interact with SmartContract

# To Do: Implement Polymorphism
def call_app_method(client, index, _method, arg1 , arg2):

    print ("Creating application call to App:", index)

    # create an instance of AtomicTransactionComposer
    atc = AtomicTransactionComposer()

    atc.add_method_call(
        app_id = index,
        method= _method, #contract.get_method_by_name(_method),
        sender = sender,
        sp = _params,
        signer = signer,
        method_args = [arg1, arg2],
        
        
        #boxes = [[0, "board"]], #https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/#smart-contract-arrays

        )

        


    #send transaction
    results = atc.execute(client, 2)

    #wait for confirmation
    print("TXID: ", results.tx_ids[0])
    print("Result confirmed in round: {}".format(results.confirmed_round))



# convert 64 bit integer i to byte string
def intToBytes(i):
    return i.to_bytes(8, "big")



# convert game board to integer

def boardToint(string_list : list):
    #string_list = ["X", "O", "", "", "", "", "", "", ""]
    
    #print ("debug: ",string_list)
    board_ = 0
    
    for i in range(9):
        #print (i)    
        if string_list[i] == "X":
            board_ += 1 * (3 ** i)
        elif string_list[i] == "O":
            board_ += 2 * (3 ** i)

    return board_



def intToBoard(board_as_int : int):
    string_list = [""] * 9
    for i in range(9):
        digit = board_as_int % 3
        if digit == 1:
            string_list[i] = "X"
        elif digit == 2:
            string_list[i] = "O"
        board_as_int //= 3

    return string_list


def synchronize_game_state(client, app_id : int , board: int, game_state : int)-> None:
    


    fee = 1000

    print ("Synchronizing Game State")

    # Save Current Board Bytes to Smart Contract

    call_app_method(client, app_id, Sync_method, board , game_state)


    # Synchronize client board state with App State




if __name__ == "__main__":

    



    # Build Smart Contract
    tictactoe_app = tictactoe.build()


    #print(tictactoe_app.approval_program)
    
    #print(tictactoe_app.clear_program)
    tictactoe_app.to_json()

    y= json.loads(tictactoe_app.to_json())
    
    #print(y)


    ## returns synchronize game method
    __method = (y['contract']['methods'][1])

    #print (__method)

    Sync_method =Method(
        name = __method['name'],
        args = [Argument("uint64"), Argument("uint64")], # byte encoding bug, reverting to utf8
        desc= " Syncs method calls to SmartContract",
        returns = Returns('void'),

        )
    #print (Sync_method.dictify())


    with open("approval_program.teal", "w") as f:
        f.write(tictactoe_app.approval_program)





    """
    Run Game Loop (For Testing)

    
    """


    # Create Algod Node
        # test-net
    algod_address = "https://node.testnet.algoexplorerapi.io"
    algod_token = ""
    algod_client = algod.AlgodClient(algod_token, algod_address)



    _params = algod_client.suggested_params()

    __mnemonic : str = "tank game arrive train bring taxi tackle popular bacon gasp tell pigeon error step leaf zone suit chest next swim luggage oblige opinion about execute"

    # For Testing
    app_id : int = 194435708 #194398904


    # Generate Account for Playing
    accts = {}
    accts[1] = {}    
    accts[1]['sk'] = mnemonic.to_private_key(__mnemonic) #saves the new account's mnemonic
    accts[1]['pk'] = account.address_from_private_key(accts[1]['sk']) #saves the new account's address


  


        # create a Signer Object
    signer = AccountTransactionSigner(accts[1]['sk'])


    # get sender address
    sender = accts[1]['pk'] #account.address_from_private_key(private_key)



    #params = client.suggested_params()

    _params.flat_fee = True
    _params.fee = 1000

    command = input("Enter command  [ play , continue ,reset, deploy, quit ]  ")
    
    "*****************Perform Transactions Operations**********************"

    match command:
        case "deploy":
    


                

                # Deploy Smart Contract if not already deployed
                
                app_id = deploy(_params, accts[1]['sk'],  algod_client, 1000, 4,10)


        case "play":

         board : list[str] = [' '] * 9

         tictactoe_client(board)


        case "delete":
            delete_app(algod_client, accts[1]['sk'], app_id)


        case "reset":
            synchronize_game_state(algod_client,app_id, 0, 0)

        case "continue":

            # load board from smart contract globals

             data =algod_client.application_info(app_id)
             
             board : list[str] = (intToBoard(data['params']['global-state'][0]['value']['uint']))

             # send board data and start game

             tictactoe_client(board)

        case "quit":
             quit()
