import json
import requests
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv('.env')

# Replace the following variables with the appropriate values
contract_address = "0xDafdC2Ae8ceEB8c4F70c8010Bcd7aD6853CeF532"
infura_rpc_url = os.getenv("REACT_APP_GORELI")
api_url = "https://reputable-swagger-api.onrender.com/reputation_score"

# Contract ABI as provided in the question
contract_compiled_path = './src/abi/WebInterface.json'
with open(contract_compiled_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']

def handle_event(event):
    # Get the seller ID from the event data
    seller_id = event['args'].sellerId

    # Make the POST request to the API
    post_data = {
        "sellerId": seller_id
    }
    try:
        response = requests.post(api_url, json=post_data, timeout=60)  # Set a reasonable timeout value
        response.raise_for_status()  # Raise an exception if the request was not successful
        if response.status_code == 200:
            print(f"Successfully sent seller ID {seller_id} to the API.")
        else:
            print(f"Failed to send seller ID {seller_id} to the API. Status Code: {response.status_code}")
    except requests.exceptions.Timeout:
        print("Request to API timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Error making the API request: {e}")


   

def main():
    # Connect to the Ethereum node using Infura HTTP provider
    web3 = Web3(Web3.HTTPProvider(infura_rpc_url))

    # Instantiate the contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

     # Subscribe to the ScoreAdded event
    event_filter = contract.events.ScoreAdded.createFilter(fromBlock="latest")

    print("Listening for ScoreAdded events...")

    while True:
        try:
            for event in event_filter.get_new_entries():
                print(event['args'].sellerId)
                handle_event(event)
        except KeyboardInterrupt:
            print("Stopped listening.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
