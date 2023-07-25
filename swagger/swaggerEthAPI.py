# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 02:49:51 2021

@author: prince
"""
# Flask API integration with Swagger
from web3 import Web3, HTTPProvider
from flask import Flask, request, jsonify, render_template, redirect, url_for
# from flask_swagger_ui import get_swaggerui_blueprint
from pathlib import Path
from phe import paillier
import phe
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import time
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
load_dotenv('.env')


seller_to_address = {
  "11": "0xb7a000c543ac7e39fdf4fc391b3900078e070325",
  "12": "0x1ef94bea1542da6d61c68f26f7a3933a240c87bd",
  "13": "0x710dd7f6e3e47ddc08fac4795694d7ec4506c4e6"
}


mnemonic_phrase = os.getenv("REACT_APP_MNEMONIC_PHRASE")
sepolia_testnet_url = os.getenv("REACT_APP_SEPOLIA")

if not mnemonic_phrase:
    print("Please provide the mnemonic phrase in the .env file.")
    exit(1)

# Connect to the Sepolia Testnet using web3.py
web3 = Web3(Web3.HTTPProvider(sepolia_testnet_url))
web3.eth.account.enable_unaudited_hdwallet_features()


# Account from mnemonic phrase
account = web3.eth.account.from_mnemonic(mnemonic_phrase)

oracle_address = os.getenv('REACT_APP_GORELI_ORACLE_ADDRESS')
gateway_address = os.environ.get('REACT_APP_GORELI_GATEWAY_ADDRESS')
onchain_address = os.environ.get('REACT_APP_GORELI_ONCHAIN_ADDRESS')
web_address = os.environ.get('REACT_APP_GORELI_WEB_ADDRESS')

print(f"Envionment variables initialized")

# https://deapsecure.gitlab.io/deapsecure-lesson05-crypt/21-paillier-he/index.html

# pub,priv = paillier.generate_paillier_keypair(n_length=256)


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

cred = credentials.Certificate('reputable.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection("individual_scores").document("mjHPrqCFPf8y3vAJ9vE1")
if doc_ref is not None:
    print("document initialized")
    #print(doc_ref.get().to_dict())

# blockchain_address = 'HTTP://127.0.0.1:8545'
# # Client instance to interact with the blockchain
# web3 = Web3(HTTPProvider(blockchain_address))

# web3.eth.defaultAccount = web3.eth.accounts[0]

oracle_compiled_path = 'src/abi/OracleInterface.json'
# oracle_address = '0xE31f1289B6cF7c312f9998bD7F8CaaB14BCf30C5'
with open(oracle_compiled_path) as file:
    oracle_json = json.load(file)  # load contract info as JSON
    oracle_abi = oracle_json['abi']

oracle_contract = web3.eth.contract(address=oracle_address, abi=oracle_abi)

gateway_compiled_path = 'src/abi/GatewayInterface.json'
# gateway_address =  '0xbEdC585D53AD54b9F276807AC8e9E42a0A2Eb95F'
with open(gateway_compiled_path) as file:
    gateway_json = json.load(file)  # load contract info as JSON
    gateway_abi = gateway_json['abi']
gateway_contract = web3.eth.contract(address=gateway_address, abi=gateway_abi)


onchain_compiled_path = 'src/abi/OnChainReputationData.json'
# onchain_address = '0x9948689B9a14D40fB84cD848a3e0431A0492136F'
with open(onchain_compiled_path) as file:
    onchain_json = json.load(file)  # load contract info as JSON
    onchain_abi = onchain_json['abi']
onchain_contract = web3.eth.contract(address=onchain_address, abi=onchain_abi)


web_compiled_path = 'src/abi/WebInterface.json'
# web_address = '0x9d59C6168e100B68E431Cfbdb749C8CB3143FbB6'
with open(web_compiled_path) as file:
    web_json = json.load(file)  # load contract info as JSON
    web_abi = web_json['abi']
web_contract = web3.eth.contract(address=web_address, abi=web_abi)

firestore_path = "https://firestore.googleapis.com/v1/projects/reputable-b7df1/databases/(default)/documents/individual_scores/mjHPrqCFPf8y3vAJ9vE1"

app = Flask(__name__)


@ app.route('/')
# @app.route('/static/<path:path>')
def home():
    # return "<h1>Hello World</h1>"
    return redirect("/docs")


@ app.route('/docs')
# @app.route('/static/<path:path>')
def index():
    # API_URL = "/static/swagger.json or yaml"

    # SWAGGER_URL = '/swagger'
    # swaggerui_blueprint = get_swaggerui_blueprint(
    #     SWAGGER_URL,
    #     API_URL,
    #     config={
    #         'app_name': "Reputable Swagger API"})
    return render_template('swaggerui.html')


@ app.route("/oracle", methods=['POST', 'GET'])
def oracle_address():
    # address = request.args.get("address")
    address = oracle_address
    address = web3.toChecksumAddress(address)
    # post
    # sets the address of oracle on web int

    # = onchain_contract.functions.get_rep_data(seller_id).call()
    # web_contract.functions.setOracleAddress(address).transact()

    try:

        # Build the transaction
        transaction = web_contract.functions.setOracleAddress(address).buildTransaction({
                "chainId": 5,  # Replace with the chain ID of the Sepolia Testnet
                "gas": 2000000,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.getTransactionCount(account.address),
            })

        # Sign the transaction
        signed_transaction = account.sign_transaction(transaction)

        # Send the signed transaction
        tx_hash = web3.eth.send_raw_transaction(
            signed_transaction.rawTransaction)
        tx_receipt=web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transaction receipt:", tx_receipt)
    except Exception as e:
        print("Error while sending transaction:", e)

                # sellerid, token_val, user_id, uint val(1 or 0)
                # userid example 1234
                # token example 104

    print("Im where dummy data supposed to be")
    # web_contract.functions.adder(11, 100, 1200, 1).transact()
    # web_contract.functions.adder(11, 101, 1201, 1).transact()
    # web_contract.functions.adder(11, 102, 1202, 1).transact()
    # web_contract.functions.adder(11, 103, 1203, 0).transact()
    # web_contract.functions.adder(11, 104, 1204, 1).transact()
    # calls the add data several times to add dummy data
    # will later be called on front end web interface
    return jsonify({"result": "success"})

    # return "Hello World"

    # app.register_blueprint(request_api.get_blueprint())

    # return render_template('index.html')
    # with open(os.path.dirname(app.root_path) + '/readme.md', 'r') as file:
    #     content = file.read();
    #     return markdown.markdown(content)
    # return "Hello World"
    pass


@ app.route("/test")
# @cross_origin()
def test():
    seller_id=request.args.get("sellerId")
    doc_ref=db.collection("individual_scores").document(
        "mjHPrqCFPf8y3vAJ9vE1")
    # emp_ref = db.collection('individual socre')
    # docs = doc_ref.stream()
    docs = doc_ref.get()
    docs = docs.to_dict()
    doc_list = []
    # for doc in docs:
    #     print('{} => {} '.format(doc.id, doc.to_dict()))
    #     doc_list.append(doc)
    data = docs['data']
    h = ''
    t = ''
    # loop through dta
    # compare with seller id
    # return the hash and timestamp
    # data0 = data[0]
    # print(doc_list)

    # for i in data:
    #    doc_list.append(i)
    for i in data:
        # print(type(seller_id))
        if i['seller_id'] == int(seller_id):
            print("seller_id: ", i['seller_id'])
            print("hash: ", i['tx_hash'])
            h = i['tx_hash']
            t = i['Timestamp']
            break
    # for now only returns the first data meeting the criteria
    return jsonify({"hash": h, "timestamp": t})
    # return jsonify({"data": data})#jsonify({"test": 123})


@app.route("/reputation")
# GET
def get_rep():
    # try catch gets seller id from the post
    # uses seller id to make a request to the ... smart contract with web3
    # score = get_rep_data(seller_id)
    # return jsonify("score": score)
    seller_id = request.args.get("sellerId")
    print(seller_id)
    rep = onchain_contract.functions.get_rep_data(int(seller_id)).call()
    print("rep" + rep)  # fails if rep is empty
    enc_score = paillier.EncryptedNumber(pub, int(rep))
    dec_score = priv.decrypt(enc_score)
    return jsonify({"score": dec_score})
    # return jsonify({"reputation score": rep})


CORS(app, support_credentials=True, resources=r'/verify_reputation/*')


@cross_origin()
@app.route("/verify_reputation")
# get Request
def verifyReputation():
    ethereum_address = request.args.get("ethereumAddress")
    # Get the seller ID from the dictionary using the Ethereum address
    seller_id = next((k for k, v in seller_to_address.items() if v == ethereum_address), None)
    if seller_id is None:
        return jsonify({"error": "Seller not found with the given Ethereum address"})
   #seller_id = request.args.get("sellerId")
    doc_ref = db.collection("individual_scores").document(
        "mjHPrqCFPf8y3vAJ9vE1")
    # emp_ref = db.collection('individual socre')
    # docs = doc_ref.stream()
    docs = doc_ref.get().to_dict()
    # docs = docs.to_dict()
    doc_list = []
    # for doc in docs:
    #     print('{} => {} '.format(doc.id, doc.to_dict()))
    #     doc_list.append(doc)
    data = docs['data']
    h = ''
    t = ''
    # loop through dta
    # compare with seller id
    # return the hash and timestamp
    # data0 = data[0]
    # print(doc_list)

    # for i in data:
    #    doc_list.append(i)
    for i in data:
        # print(type(seller_id))
        if i['seller_id'] == int(seller_id):
            print("seller_id: ", i['seller_id'])
            print("hash: ", i['tx_hash'])
            h = i['tx_hash']
            t = i['Timestamp']
            break
    score = onchain_contract.functions.get_rep_data(int(seller_id)).call()
    enc_score = paillier.EncryptedNumber(pub, int(score))
    dec_score = priv.decrypt(enc_score)
    # return jsonify({"score": dec_score})
    # for now only returns the first data meeting the criteria
    return jsonify({"hash": h, "timestamp": t, "score": dec_score})
    # return jsonify("value": doc)


@app.route("/individual_score")
def get_ind_score():
    # get and takes seller id and user id

    seller_id = request.args.get("sellerId")
    user_id = request.args.get("userId")
    doc_ref = db.collection("individual_scores").document(
        "mjHPrqCFPf8y3vAJ9vE1")
    # emp_ref = db.collection('individual socre')
    # docs = doc_ref.stream()
    docs = doc_ref.get().to_dict()
    # docs = docs.to_dict()
    data = docs['data']

    # loop through dta
    # compare with seller id
    # return the hash and timestamp
    # data0 = data[0]
    # print(doc_list)
    ind_score = None
    # for i in data:
    #    doc_list.append(i)
    for i in data:
        # print(type(seller_id))
        if i['seller_id'] == int(seller_id):
            if i['user_id'] == int(user_id):
                print("indiv score: ", i['individual_score'])
                ind_score = i['individual_score']
    #for now only returns the first data meeting the criteria
    # enc_score = paillier.EncryptedNumber(pub, int(score))
    # dec_score = priv.decrypt(enc_score)
    #return jsonify({"individual score": dec_score})

        #implement getting data from the json data on firebase (firestore)
    return jsonify({"indiviual score": ind_score})#, "timestamp": t})

@app.route("/individual_scores")
def get_ind_scores():
    #Get takes sellerId
    #sellerId
    #Makes a call to the deployed data service contract
    #score = contract.get_data(seller_id)
    #jsonify "scores": scores_array
    ind_scores = []
    seller_id = request.args.get("sellerId")
    doc_ref = db.collection("individual_scores").document("mjHPrqCFPf8y3vAJ9vE1")
    #emp_ref = db.collection('individual socre')
    #docs = doc_ref.stream()
    docs = doc_ref.get().to_dict()
    #docs = docs.to_dict()
    data = docs['data']
    
    for i in data:
        print("length data: ", len(data))
        if i['seller_id'] == int(seller_id):
            ind_scores.append(i['individual_score'])
            
    #for now only returns the first data meeting the criteria

        #implement getting data from the json data on firebase (firestore)
    return jsonify({"indiviual score": ind_scores})#, "timestamp": t})
CORS(app, support_credentials=True, resources=r'/reputation_score/*')
@app.route("/reputation_score", methods=['POST', 'GET'])
@cross_origin()
#POST
def rep_score_post():
    #if request.method == "POST":
    try:
    #seller_id = request.values.get("sellerId")
        seller_id = request.json.get('sellerId')
    except:
        seller_id = request.args.get('sellerId')
    print("seller_ID: ", seller_id)
    #seller_scores = request.args.get("sellerScores")
    print("type: ", type(seller_id))
    seller_id = int(seller_id)
    try:
    #print("sellerId: ", int)
    #ind_scores = request.args.get('userScores')
    #call aggr function from web interface
        # transaction = web_contract.functions.aggr(seller_id).transact()
        # web3.eth.waitForTransactionReceipt(transaction)
        # receipt = web3.eth.getTransactionReceipt(transaction)
        # print('Transaction receipt:', receipt)
        try:

            # Build the transaction
            transaction = web_contract.functions.aggr(seller_id).buildTransaction({
                "chainId": 5,  # Replace with the chain ID of the Sepolia Testnet
                "gas": 2000000,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.getTransactionCount(account.address),
            })

            # Sign the transaction
            signed_transaction = account.sign_transaction(transaction)

            # Send the signed transaction
            tx_hash = web3.eth.send_raw_transaction(
                signed_transaction.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print("Transaction receipt:", tx_receipt)
        except Exception as e:
            print("Error while sending transaction:", e)

        #time.sleep(2)
        score = onchain_contract.functions.get_rep_data(seller_id).call()
        print("score" + score)
        #time.sleep(2) 
        #wait 2 secs
            #call the onchain function to get the aggr score.
            ##Send this to the aggregator
            ##score = call onchain function to get the aggr score
        #else:
        #    score = "Only Post requests"
        
        #make it into an enc number using pub. Decrypt
        enc_score = paillier.EncryptedNumber(pub, int(score))
        dec_score = priv.decrypt(enc_score)
    except:
        raise ValueError("Seller not rated by buyers yet!")
    return jsonify({"score": dec_score})
    #return jsonify({"score": score})
@app.route("/token_used")
def is_token_used():
    #takes in a token and a seller id
    #returns a token array
    #loop through the token
    #if the token and at array ==
    #variable = true
    #compares each one while assigning the bool to a variable
    #return jsonify "used": true
    seller_id = request.args.get("sellerId")
    seller_id = int(seller_id)
    token_val = request.args.get("token")
    token_val = int(token_val)
    used = web_contract.functions.isUsed(seller_id, token_val).call()
    if used is True:
        used_return = True
    else:
        used_return = False
    
    return jsonify({"used": used_return})

#addpositiveScore(sellerID, token) - uses isTokenUsed
#addNegativeScore(sellerId, token)
#Add aggrScore(sellerId, enc_aggr_score)
#EncryptZero(returns encrypted number in json)
#EnccryptOne(returns encrypted 0 in json)
    
    
#add other endpoints
#aggregate endpoints with json data passed to it.
#handle with try/catch data being sent.

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)