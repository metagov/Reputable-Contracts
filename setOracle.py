from web3 import Web3
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')

# Connect to the local Ganache blockchain
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))


# Set the default account (so we don't need to set the "from" for every transaction call)
w3.eth.defaultAccount = w3.eth.accounts[0]

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
transaction = web_contract.functions.setOracleAddress(oracle_address).transact()

# Wait for the transaction to be mined
w3.eth.waitForTransactionReceipt(transaction)

# Print the transaction receipt
receipt = w3.eth.getTransactionReceipt(transaction)
print('Transaction receipt:', receipt)
