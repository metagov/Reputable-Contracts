from web3 import Web3, HTTPProvider
from pathlib import Path
import time
from phe import paillier
import json
from web3.logs import DISCARD
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import phe
import requests
import os
from dotenv import load_dotenv
load_dotenv('.env')

mnemonic_phrase = os.getenv("REACT_APP_MNEMONIC_PHRASE")
sepolia_testnet_url = os.getenv("REACT_APP_SEPOLIA")
goreli_testnet_url = os.getenv("REACT_APP_GORELI")
etherscan_url = f"https://sepolia.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash="

if not mnemonic_phrase:
    print("Please provide the mnemonic phrase in the .env file.")
    exit(1)

# Connect to the Sepolia Testnet using web3.py
web3 = Web3(Web3.HTTPProvider(goreli_testnet_url))
web3.eth.account.enable_unaudited_hdwallet_features()
network_id = web3.eth.chainId
print("Active on Network ID:", network_id)
# Account from mnemonic phrase
account = web3.eth.account.from_mnemonic(mnemonic_phrase)

oracle_address = os.getenv('REACT_APP_GORELI_ORACLE_ADDRESS')
gateway_address = os.environ.get('REACT_APP_GORELI_GATEWAY_ADDRESS')
onchain_address = os.environ.get('REACT_APP_GORELI_ONCHAIN_ADDRESS')
web_address = os.environ.get('REACT_APP_GORELI_WEB_ADDRESS')

print(f"Environment varibales initialized")


def make_post_request(seller_id):
    url = f'https://reputable-swagger-api.onrender.com/reputation_score?sellerId='+str(seller_id)
    headers = {'accept': 'application/json'}
    data = ''

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print(f'Posted Reputation')
            return None
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
            return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

async def GetGasPrice():
    try:
        gas_price = await web3.eth.gas_price
        return gas_price
    except Exception as e:
        print("Error calculating Gas Price:", str(e))


def aggregate(seller_addr, ind_data):
    # ind_data = array of ind scores
    aggr_score = pub.encrypt(0)
    # checks the exp responses for the seller
    # fetch data from ind_score beforehand
    # fetch expected responses from smart contract
    # exp_res = 12 #get exp responses for seller
    # get_response count not defined (only on smart contract)
    # get ind scores from seller
    # function to be pulled from smart contract e.g.
    # filled for seller. Could be dict key val of seller

    # loop through the ind score for the seller and use
    # additive hom enc to get an aggr score
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
# tbd


def handle_event(event):
    print("Recieved Event!")
    # Parse parameters inside event
    receipt = web3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = RequestValueEvent.processReceipt(receipt, errors=DISCARD)

    if len(result) == 0:
        result = RequestScoreEvent.processReceipt(receipt, errors=DISCARD)
        doc_ref = db.collection("individual_scores").document(
            "offChainData")

        args = result[0]["args"]
        seller_id = args["sellerId"]
        individual_score = args["indi_score"]
        token_val = args["token_val"]
        user_id = args["user_id"]

        enc_score = str(encrypt_score(individual_score))

        try:

            # Build the transaction
            transaction = web_contract.functions.add(seller_id, token_val, user_id, enc_score).buildTransaction({
                "chainId": 5,  # Replace with the chain ID of the Sepolia Testnet
                "gas": 5000000,
                "gasPrice": web3.eth.gas_price*2,
                "nonce": web3.eth.getTransactionCount(account.address),
            })

            # Sign the transaction
            signed_transaction = account.sign_transaction(transaction)

            # Send the signed transaction
            tx_hash = web3.eth.send_raw_transaction(
                signed_transaction.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            if tx_receipt:
                print("Transaction receipt recieved for add()")
                print("Making POST request for "+ str(seller_id))
                if (type(seller_id )!= 'NoneType'):
                    make_post_request(seller_id)

            else:
                print("Transaction reciept not recieved for add()")
        except Exception as e:
            print(
                "Error while sending Add transaction, when handling RequestScoreEvent:", e)

        # web_contract.functions.add(seller_id, token_val, user_id, enc_score)act()

        # with open("individual.json", "r+") as file:
        #     json_data1 = json.load(file)
        #     print(json_data1)
        #     print(type(json_data1['data']))
        #     json_data1["data"].append({
        #         "seller_id": seller_id,
        #         "token_val": token_val,
        #         "user_id": user_id,
        #         "enc_score": enc_score
        #         })
        #     json.dump(json_data1, file)
        #     doc_ref.set(json_data1)

    else:

        try:
            doc_ref = db.collection("individual_scores").document(
                "offChainData")
            args = result[0]["args"]

            # campaign_id = args["campaignId"]
            seller_id = args["sellerId"]
            user_id = args["userId"]
            enc_scores = args["array"]

            off_chain_path = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/individual_scores/offChainData"
            aggr_score = str(aggregate(seller_addr=None, ind_data=enc_scores))
            print("Aggregate Score: ", aggr_score)
            timestamp = str(datetime.now())

            # Once result has been retrieved, return this back into smart contract
            # tx_hash = oracle_contract.functions.returnToGateway(
            #     gateway_address, aggr_score, off_chain_path)act()
            # print("Transaction Hash: ", web3.toHex(tx_hash))

            try:

                # Build the transaction
                transaction = oracle_contract.functions.returnToGateway(
                    gateway_address, aggr_score, off_chain_path).buildTransaction({
                        "chainId": 5,  # Replace with the chain ID of the Sepolia Testnet
                        "gas": 5000000,
                        "gasPrice": web3.eth.gas_price*2,
                        "nonce": web3.eth.getTransactionCount(account.address),
                    })

                # Sign the transaction
                signed_transaction = account.sign_transaction(transaction)

                # Send the signed transaction
                tx_hash = web3.eth.send_raw_transaction(
                    signed_transaction.rawTransaction)
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                if tx_receipt:
                    print("Transaction receipt recieved for returnToGateway()")
                else:
                    print("Transaction reciept not recieved for returnToGateway()")
            except Exception as e:
                print(
                    "Error while sending ReturnToGateway transaction, when handling RequestValueEvent:", e)

                # Transfer to onchain smart contract
                # onchain_contract.functions.add_rep_data(
                #     seller_id, aggr_score).transact()

            try:

                # Build the transaction
                transaction = onchain_contract.functions.add_rep_data(
                    seller_id, aggr_score).buildTransaction({
                        "chainId": 5,  # Replace with the chain ID of the Sepolia Testnet
                        "gas": 5000000,
                        "gasPrice": web3.eth.gas_price*2,
                        "nonce": web3.eth.getTransactionCount(account.address),
                    })

                # Sign the transaction
                signed_transaction = account.sign_transaction(transaction)

                # Send the signed transaction
                tx_hash = web3.eth.send_raw_transaction(
                    signed_transaction.rawTransaction)
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                if tx_receipt:
                    print("Transaction receipt recieved for add_rep_data()")
                else:
                    print("Transaction reciept not recieved for add_rep_data()")

            except Exception as e:
                print(
                    "Error while sending Add_Rep_data transaction, when handling RequestValueEvent:", e)

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
# geth_path = "C:\\Users\\prince\\Documents\\geth.ipc"
# geth_path = '\\\\.\\pipe\\geth.ipc'
# geth_path = "./reputablechain/geth.ipc"
# geth_path = "\\.\pipe\geth.ipc"
# geth_path = "\\\\.\\pipe\\geth.ipc"
# geth_path = "/home/prince/.ethereum/goerli/geth.ipc"
# w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/96b121e6b8114768923adf1cb21b034d'))
# w3 = Web3(Web3.IPCProvider('/home/ja25499/.ethereum/goerli/geth.ipc'))
# w3 = Web3(Web3.IPCProvider(geth_path))


# This will allow it to work on Rinkeby and other PoA testnets
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# w3.eth.defaultAccount = "0x6E3a1Ce9FAB10c777d7b89c899A8EC71c6672283"
# 0x1163c525808b6fC15002137757b30793DE506F72

# w3.eth.defaultAccount = "0x1163c525808b6fC15002137757b30793DE506F72"
# w3.eth.defaultAccount = "0x6E3a1Ce9FAB10c777d7b89c899A8EC71c6672283"
# Account must be unlocked to allow for transactions
# Password set to: 'Password1' and '0' sets account to be be unlocked indefinitely
# w3.geth.personal.unlock_account(w3.eth.defaultAccount, "Password1", 0)
# w3.geth.personal.unlock_account(w3.eth.defaultAccount, "Password1", 0)
# "Password1"
# blockchain_address = 'HTTP://127.0.0.1:8545'
# # Client instance to interact with the blockchain
# web3 = Web3(HTTPProvider(blockchain_address))
# # Set the default account (so we don't need to set the "from" for every transaction call)
# web3.eth.defaultAccount = web3.eth.accounts[0]

oracle_compiled_path = './src/abi/OracleInterface.json'
# oracle_address = '0x16aed03fe56C02A49362fE224a12F70e76Dbc7dB'
with open(oracle_compiled_path) as file:
    oracle_json = json.load(file)  # load contract info as JSON
    oracle_abi = oracle_json['abi']
    # print("oracle_abi: ", oracle_abi)
oracle_contract = web3.eth.contract(address=oracle_address, abi=oracle_abi)
# getSellerId()


gateway_compiled_path = './src/abi/GatewayInterface.json'
# gateway_address = '0x40aF400fAE11C9FfAB4764b47C1A3b3305DA6C79'
with open(gateway_compiled_path) as file:
    gateway_json = json.load(file)  # load contract info as JSON
    gateway_abi = gateway_json['abi']
gateway_contract = web3.eth.contract(address=gateway_address, abi=gateway_abi)


onchain_compiled_path = './src/abi/OnChainReputationData.json'
# onchain_address = '0xAe32Dd1169f65E5Cbd71790E87Aaf3C737a99730'
with open(onchain_compiled_path) as file:
    onchain_json = json.load(file)  # load contract info as JSON
    onchain_abi = onchain_json['abi']
onchain_contract = web3.eth.contract(address=onchain_address, abi=onchain_abi)


web_compiled_path = './src/abi/WebInterface.json'
# web_address = '0x46B6E377b14081EFBd2D08D096294Ae228627e43'
with open(web_compiled_path) as file:
    web_json = json.load(file)  # load contract info as JSON
    web_abi = web_json['abi']
web_contract = web3.eth.contract(address=web_address, abi=web_abi)


def keypair_load_pyp(pub_jwk, priv_jwk):
    """Deserializer for public-private keypair, from JWK format."""
    rec_pub = json.loads(pub_jwk)
    rec_priv = json.loads(priv_jwk)
    pub_n = phe.util.base64_to_int(rec_pub['n'])
    pub = paillier.PaillierPublicKey(pub_n)
    priv_p = phe.util.base64_to_int(rec_priv['p'])
    priv_q = phe.util.base64_to_int(rec_priv['q'])
    priv = paillier.PaillierPrivateKey(pub, priv_p, priv_q)
    return pub, priv


with open("phe_key.pub", "r") as f:
    pub_jwk = f.read()

with open("phe_private_key.priv", "r") as f:
    priv_jwk = f.read()

pub, priv = keypair_load_pyp(pub_jwk, priv_jwk)

# pub,priv = paillier.generate_paillier_keypair(n_length=256)


cred = credentials.Certificate('./src/abi/reputable.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection("individual_scores").document("offChainData")


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
# JSON file to store individual feedback
with open("individual.json", "w") as file:
    json_data = {"data": []}
    json.dump(json_data, file)

with open("off-chain.json", "w") as file:
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
