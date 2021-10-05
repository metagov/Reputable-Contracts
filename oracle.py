from web3 import Web3, HTTPProvider
from pathlib import Path
from web3.middleware import geth_poa_middleware
import time
from phe import paillier
import json
from web3.logs import DISCARD
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime



def aggregate(seller_addr, ind_data):
    #ind_data = array of ind scores
    aggr_score = pub.encrypt(0)
    #checks the exp responses for the seller 
    #fetch data from ind_score beforehand
    #fetch expected responses from smart contract
    #exp_res = 12 #get exp responses for seller
    #get_response count not defined (only on smart contract)
        #get ind scores from seller
        #function to be pulled from smart contract e.g.
        #filled for seller. Could be dict key val of seller
        
        #loop through the ind score for the seller and use
        #additive hom enc to get an aggr score
    for i in ind_data:
        ind = paillier.EncryptedNumber(pub, int(i))
        aggr_score += ind
    
    return str(aggr_score.ciphertext())


def encrypt_score(score):
    return pub.encrypt(int(score)).ciphertext()

def encryptZero():
    zero = pub.encrypt(0)
    return zero.ciphertext()
    
def encryptOne():
    one = pub.encrypt(1)
    return one.ciphertext()
#tbd


def handle_event(event):
    print("Recieved Event!")
    # Parse parameters inside event
    receipt = web3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = RequestValueEvent.processReceipt(receipt, errors=DISCARD)
    

    if len(result) == 0:
        result = RequestScoreEvent.processReceipt(receipt, errors=DISCARD)
        doc_ref = db.collection("individual_scores").document("jz9uo3kVGcD65PW0kkEg")

        args = result[0]["args"]
        seller_id = args["sellerId"]
        individual_score = args["indi_score"]
        token_val = args["token_val"] 
        user_id = args["user_id"]
    
        enc_score = str(encrypt_score(individual_score))
    
        web_contract.functions.add(seller_id, token_val, user_id, enc_score).transact()

        with open("individual.json", "r+") as file:
            json_data = json.load(file)

            json_data.append({
                "seller_id": seller_id,
                "token_val": token_val,
                "user_id": user_id,
                "enc_score": enc_score
                }) 

            json.dump(json_data, file)
            doc_ref.set(json_data)


    else:    
        try:
            doc_ref = db.collection("individual_scores").document("mjHPrqCFPf8y3vAJ9vE1")
            args = result[0]["args"]
    
            # campaign_id = args["campaignId"]
            seller_id = args["sellerId"]
            user_id = args["userId"]
            enc_scores = args["array"]
    
            off_chain_path = "https://firestore.googleapis.com/v1/projects/reputable-b7df1/databases/(default)/documents/individual_scores/mjHPrqCFPf8y3vAJ9vE1"
            
            aggr_score = str(aggregate(seller_addr=None, ind_data=enc_scores))
            print("Aggregate Score: ", aggr_score)

            timestamp = str(datetime.now())
    
            # Once result has been retrieved, return this back into smart contract
            tx_hash = oracle_contract.functions.returnToGateway(gateway_address, aggr_score, off_chain_path).transact()
            print("Transaction Hash: ", web3.toHex(tx_hash))
            
            # Transfer to onchain smart contract
            onchain_contract.functions.add_rep_data(seller_id, aggr_score).transact()
    
            with open("off-chain.json", "r+") as file:
                json_data = json.load(file)
    
                for i, _id in zip(enc_scores, user_id):
                    json_data["data"].append({
                        "Timestamp": timestamp,
                        # "campaign_id": campaign_id, 
                        "seller_id": seller_id, 
                        "user_id": _id,
                        "individual_score": str(i),
                        "tx_hash": web3.toHex(tx_hash)
                        })
    
                file.seek(0)
                json.dump(json_data, file)
    
                doc_ref.set(json_data)
    
    
            # Write data off-chain onto a local csv file
            # with open("off-chain.csv", "a", newline='') as file:
            #     writer = csv.writer(file)
    
            #     for i in enc_scores:
            #         writer.writerow([campaign_id, seller_id, user_id, encrypt_score(i), w3.toHex(tx_hash)])
    
            
            print("Request has been successful!")
    
            # []
    
            # balance = w3.eth.get_balance(w3.eth.defaultAccount)
            # print("The balance is now: ", balance)
        
        except IndexError:
            pass



# Poll for events and pass these onto 'handle_event' function
def log_loop(event_filter, poll_interval):

    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)

        time.sleep(poll_interval)



# Uses a geth node running locally
#geth_path = "C:\\Users\\prince\\Documents\\geth.ipc"
#geth_path = '\\\\.\\pipe\\geth.ipc'
#geth_path = "./reputablechain/geth.ipc"
#geth_path = "\\.\pipe\geth.ipc"
#geth_path = "\\\\.\\pipe\\geth.ipc"
#geth_path = "/home/prince/.ethereum/goerli/geth.ipc"
# w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/96b121e6b8114768923adf1cb21b034d'))
#w3 = Web3(Web3.IPCProvider('/home/ja25499/.ethereum/goerli/geth.ipc'))
#w3 = Web3(Web3.IPCProvider(geth_path))


# This will allow it to work on Rinkeby and other PoA testnets
#w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#w3.eth.defaultAccount = "0x6E3a1Ce9FAB10c777d7b89c899A8EC71c6672283"
#0x1163c525808b6fC15002137757b30793DE506F72

#w3.eth.defaultAccount = "0x1163c525808b6fC15002137757b30793DE506F72"
#w3.eth.defaultAccount = "0x6E3a1Ce9FAB10c777d7b89c899A8EC71c6672283"
# Account must be unlocked to allow for transactions
# Password set to: 'Password1' and '0' sets account to be be unlocked indefinitely
#w3.geth.personal.unlock_account(w3.eth.defaultAccount, "Password1", 0)
#w3.geth.personal.unlock_account(w3.eth.defaultAccount, "Password1", 0)
#"Password1"

blockchain_address = 'HTTP://127.0.0.1:8545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]

oracle_compiled_path = './src/abi/OracleInterface.json'
oracle_address = '0x78CD3d5c00269ba0bDe0172e504AD344cc4cbf29'
with open(oracle_compiled_path) as file:
    oracle_json = json.load(file)  # load contract info as JSON
    oracle_abi = oracle_json['abi']
    #print("oracle_abi: ", oracle_abi)
oracle_contract = web3.eth.contract(address=oracle_address, abi=oracle_abi)
#getSellerId()



gateway_compiled_path = './src/abi/GatewayInterface.json'
gateway_address = '0xc591cB045A256e6ad6448e103cAC2a77e9f37CC2'
with open(gateway_compiled_path) as file:
    gateway_json = json.load(file)  # load contract info as JSON
    gateway_abi = gateway_json['abi']
gateway_contract = web3.eth.contract(address=gateway_address, abi=gateway_abi)


onchain_compiled_path = './src/abi/OnchainReputationData.json'
onchain_address = '0x9bee4A9e2a15960565561E1b13c4dbA3809334E0'
with open(onchain_compiled_path) as file:
    onchain_json = json.load(file)  # load contract info as JSON
    onchain_abi = onchain_json['abi']
onchain_contract = web3.eth.contract(address=onchain_address, abi=onchain_abi)


web_compiled_path = './src/abi/WebInterface.json'
web_address = '0xBE14fA01dD9bb817DF0479A9fEC8472547B32ED1'
with open(web_compiled_path) as file:
    web_json = json.load(file)  # load contract info as JSON
    web_abi = web_json['abi']
web_contract = web3.eth.contract(address=web_address, abi=web_abi)

pub,priv = paillier.generate_paillier_keypair(n_length=256)



cred = credentials.Certificate('./src/abi/reputable.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
# doc_ref = db.collection("individual_scores").document("mjHPrqCFPf8y3vAJ9vE1")


# # Oracle SC will be detailed here:
# contract_address = "0x9b438F7311BA4De18f4D065A6026546d6F7Bf4a3"
# abi = Path("abi.json").read_text()
# contract_instance = w3.eth.contract(address=contract_address, abi=abi)


# # Gateway SC will be detailed here:
# gateway_address  = "0xcc6309FdA17bEF4a782A5484666f0E0Db29D2aCd"
# gateway_abi = Path("gateway_abi.json").read_text()
# gateway_instance = w3.eth.contract(address=gateway_address, abi=gateway_abi)


# on_chain_address = "0xBe52D962B6c96C82E396Aac5e5AA4bb0f3f2cE71"
# on_chain_abi = Path("onchain_abi.json").read_text()
# on_chain_instance = w3.eth.contract(address=on_chain_address, abi=on_chain_abi)


# data_service = "0x84801c4D14ccd5E217596A561174c0ac6CBdC976"
# data_service_abi = Path("data_service_abi.json").read_text()
# data_service_instance = w3.eth.contract(address=data_service, abi=data_service_abi)

# JSON file to store and append aggregate scores
with open("off-chain.json", "w") as file:
    json_data = {"data": []}
    json.dump(json_data, file)



# JSON file to store individual feedback
with open("individual.json", "w") as file:
    json_data = {"data": []}
    json.dump(json_data, file)


# # Create local csv file to store data off-chain
# with open("off-chain.csv", "w", newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["CampaignId", "SellerId", "UserId", "IndScore", "TxHash"])



RequestValueEvent = oracle_contract.events.RequestValueEvent()
RequestScoreEvent = oracle_contract.events.RequestScoreEvent()
block_filter = web3.eth.filter({"address": oracle_address})
# {"address": contract_address}

# Set to loop every 5 secs
log_loop(block_filter, 5)





