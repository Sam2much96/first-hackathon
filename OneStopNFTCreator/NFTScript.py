import hashlib
import json

import algosdk
from algosdk.v2client import algod
from beaker import sandbox


def mintNFT(algod_client, creator_address, creator_private_key, asset_name, asset_unit_name):
    #...





    params = algod_client.suggested_params()

    
    accounts = {}
    accounts[1] = {}
    accounts[1]['pk'] = mnemonic.to_public_key(creator_private_key) #saves the new account's address
    accounts[1]['sk'] = mnemonic.to_private_key(creator_private_key) #saves the new account's mnemonic


    txn =AssetConfigTxn(sender=accounts[1]['pk'],
                        sp=params,
                        total=1,           # NFTs have totalIssuance of exactly 1
                        default_frozen=False,
                        unit_name=asset_unit_name,
                        asset_name=asset_name,
                        manager=None,
                        reserve=None,
                        freeze=False,
                        clawback="",
                        url="ipfs://QmNoThogc1D7XCzQrjePPxChyGmuohX6LXqDTCLJwTUUfR", #NFT Metadata or asset url
                        metadata_hash=None,
                        decimals=0,
                        strict_empty_address_check=False)        # NFTs have decimals of exactly 0

    signed_txn = txn.sign(accounts[1]['sk'])

     # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return
    
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    #print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 

    account_info = algod_client.account_info(__account)
    idx = 0
    found_asset = None
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if scrutinized_asset['asset-id'] == assetid:
            found_asset = scrutinized_asset
            break

    if found_asset is not None:
        return "Asset ID: {}".format(found_asset['asset-id'])
    else:
        return "Asset not found"

            




def transferNFT(algod_client, creator_address, creator_private_key, receiver_address, receiver_private_key, asset_id):
    

    params = algod_client.suggested_params()


    # construct asset transfer

    asset_tx = algod_client.construct_asset_xfer( # rewrite this as a separate function
        params,
        from_address,
        to_address,
        amount_,
        asset_id
    )
    

    # construct asset optin

    optin_tx = algod_client.construct_asset_opt_in(
            params,
            receiver_address,
            asset_id
            )


    # create grouped Transaction

    txns = algod.group_transactions([asset_tx, optin_tx])


    #Sign Both Transactions with their respective Mnemonics

    txns[0] = algod_client.sign_transaction(txns[0], creator_private_key)
    txns[1] = algod_client.sign_transaction(txns[1], receiver_private_key)

    # Send Signed Transaction

    txid = algod_client.send_transactions(txns)

    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return