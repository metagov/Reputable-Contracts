from web3 import Web3
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')

# Connect to the local Ganache blockchain

mnemonic_phrase = os.getenv("MNEMONIC_PHRASE")
sepolia_testnet_url = os.getenv("SEPOLIA")
goreli_testnet_url = os.getenv("REACT_APP_GORELI")


if not mnemonic_phrase:
    print("Please provide the mnemonic phrase in the .env file.")
    exit(1)

# Connect to the Sepolia Testnet using web3.py
w3 = Web3(Web3.HTTPProvider(goreli_testnet_url))
w3.eth.account.enable_unaudited_hdwallet_features()

# Account from mnemonic phrase
account = w3.eth.account.from_mnemonic(mnemonic_phrase)
print(account.address)
# Set the default account (so we don't need to set the "from" for every transaction call)
#w3.eth.defaultAccount = w3.eth.accounts[0]

# Set the contract address and ABI
web_compiled_path = './src/abi/WebInterface.json'
web_address = os.environ.get('WEB_ADDRESS')
with open(web_compiled_path) as file:
    web_json = json.load(file)  # load contract info as JSON
    web_abi = web_json['abi']
web_contract = w3.eth.contract(address=web_address, abi=web_abi)



# Set the address value to pass to the function
oracle_address = os.getenv('ORACLE_ADDRESS')

# Call the contract function
#transaction = web_contract.functions.setOracleAddress(oracle_address).transact()

try:

    # Build the transaction
    transaction = web_contract.functions.setOracleAddress(oracle_address).buildTransaction({
        "chainId": 5,  # Replace with the chain ID of the Sepolia Testnet
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.getTransactionCount(account.address),
    })

    # Sign the transaction
    signed_transaction = account.sign_transaction(transaction)

    # Send the signed transaction
    tx_hash = w3.eth.send_raw_transaction(
        signed_transaction.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction receipt:", tx_receipt)
except Exception as e:
    print("Error while sending transaction:", e)

# Wait for the transaction to be mined
#w3.eth.waitForTransactionReceipt(transaction)

# Print the transaction receipt
# receipt = w3.eth.getTransactionReceipt(transaction)
# print('Transaction receipt:', receipt)
