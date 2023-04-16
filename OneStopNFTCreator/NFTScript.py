import hashlib
import json

import base64

from algosdk import mnemonic, account
from algosdk.transaction import AssetConfigTxn, AssetTransferTxn, AssetOptInTxn, wait_for_confirmation

from algosdk.v2client import algod
from beaker import sandbox


def mintNFT(algodClient, creatorAddress, creatorPrivateKey, assetName, assetUnitName):
    #...





    params = algodClient.suggested_params()

    print ("Minting ", assetName, " to ", creatorAddress)


    txn =AssetConfigTxn(sender=creatorAddress,
                        sp=params,
                        total=1,           # NFTs have totalIssuance of exactly 1
                        default_frozen=False,
                        unit_name=assetUnitName,
                        asset_name=assetName,
                        manager=None,
                        reserve=None,
                        freeze=False,
                        clawback="",
                        url="ipfs://QmNoThogc1D7XCzQrjePPxChyGmuohX6LXqDTCLJwTUUfR", #NFT Metadata or asset url
                        metadata_hash=None,
                        decimals=0,
                        strict_empty_address_check=False)        # NFTs have decimals of exactly 0

    signed_txn = txn.sign(creatorPrivateKey)

     # submit transaction
    txid = algodClient.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = wait_for_confirmation(algodClient, txid, 4)  
    except Exception as err:
        print(err)
        return
    
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
   
 
    print ("Asset ID: ",confirmed_txn["asset-index"])
            




def transferNFT(algodClient, SenderAddress, SenderPrivateKey, ReceiverAddress, ReceiverPrivateKey, assetID):
    

    params = algodClient.suggested_params()


    # construct asset transfer

    asset_tx = AssetTransferTxn( 
        sender=SenderAddress,
        sp=params,
        receiver=ReceiverAddress,
        amt=1,
        index=assetID
    )


    signed_asset_transfer=asset_tx.sign(SenderPrivateKey)
    


    # construct asset optin

    optin_tx = AssetTransferTxn(
            sender = ReceiverAddress,
            sp= params,
            receiver=ReceiverAddress,
            amt=0,
            index=assetID
            )

    signed_asset_optin=optin_tx.sign(ReceiverPrivateKey)


    # create grouped Transaction

   
    # Send Signed Transaction


    txid= algodClient.send_transaction(signed_asset_optin)
    txid2 = algodClient.send_transaction(signed_asset_transfer)
    
    
    print("Signed transaction with txID: {}".format(txid))

    print("Signed transaction with txID: {}".format(txid2))

    
     #wait for confirmation 
    try:
       confirmed_txn = wait_for_confirmation(algodClient, txid2, 4)  
       print ("Confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
        return



# For local testing
"""


if __name__ == "__main__":

    # Create Algod Client

    algod_address = "https://node.testnet.algoexplorerapi.io"
    algod_token = ""
    algod_client = algod.AlgodClient(algod_token, algod_address)



    _params = algod_client.suggested_params()

    __mnemonic : str = "tank game arrive train bring taxi tackle popular bacon gasp tell pigeon error step leaf zone suit chest next swim luggage oblige opinion about execute"



    __mnemonic_2 : str = "degree feature waste gospel screen near subject boost wreck proof caution hen adapt fiber fault level blind entry also embark oval board bunker absorb garage"




    # Generate Account for Playing
    accts = {}
    accts[1] = {}    
    accts[1]['sk'] = mnemonic.to_private_key(__mnemonic) #saves the new account's mnemonic
    accts[1]['pk'] = account.address_from_private_key(accts[1]['sk']) #saves the new account's address


    accts[2] = {}    
    accts[2]['sk'] = mnemonic.to_private_key(__mnemonic_2) #saves the new account's mnemonic
    accts[2]['pk'] = account.address_from_private_key(accts[2]['sk']) #saves the new account's address





    asset_id = 194442343


    #mintNFT(algod_client, accts[1]['pk'], accts[1]['sk'], "HackaCoin 4", "hc")

    transferNFT(algod_client, accts[1]['pk'], accts[1]['sk'], accts[2]['pk'], accts[2]['sk'], asset_id)



    """