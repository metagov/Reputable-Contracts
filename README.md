# REPUTABLE


## Requirements

- `Python` 3.x
- `web3.py` 5.24.0
- `python-paillier` 1.4.0
- `firebase-admin` 5.0.3
- `Remix IDE` (https://remix.ethereum.org/)
- `Windows 10`

## Run Oracle
```sh
python3 oracle.py
```
> To deploy smart contracts, use Remix IDE 

## Proprietary Oracle

The proprietary oracle consists of an oracle smart contract and an off-chain Python backend that serve the core functions of the oracle. 
This backend is responsible for performing the off-chain computation and sending the results back into the smart contract(s). This is done by utilizing the `Web3.py` library to listen for events emitted by the oracle smart contract and perform the necessary operation depending on which event was emitted. The oracle also establishes a connection to the cloud to also store some of the results off-chain.
The oracle smart contract (`oracle.sol`) is responsible for sending a request and any required parameters to the off-chain Python oracle. To accomplish this, this smart contract will emit an event depending on the service that the off-chain oracle is requested to do. There are two services that the off-chain oracle currently supports and that this smart contract will generate an event for:
- **Encryption of individual score** – This would emit the ``RequestScoreEvent`` which takes the parameters ‘sellerId’ `uint` and ‘indi_score’ `uint`. The results of each individual score would also be stored on Cloud Firestore
- **Aggregation of encrypted scores** – This would emit the ``RequestValueEvent`` which takes the parameters ‘campaignId’ `uint`, ‘sellerId `uint`’, ‘userId’ `uint` and ‘array’ `uint[]`. The results of each aggregation would also be stored on Cloud Firestore

If the aggregation service was chosen, then the aggregate score would be returned to the ‘gateway’ contract (`gateway.sol`) via the ``returnToGateway`` function. This function creates an interface to interact with the gateway contract. The transaction hash generated from the off-chain oracle interacting with this function is also stored on the cloud database.
The address for the deployed oracle smart contract must be entered for the variable `oracle_address`. 

## Gateway Smart Contract

Once the aggregate score for a seller has been calculated off-chain, the result is then stored on-chain via the gateway smart contract (gateway.sol). The gateway contract contains a ‘callback’ function to which the oracle smart contract is able to interact with to send values which it itself has received from the off-chain oracle.
The callback functions contains **two** parameters:
- ``_aggr_score`` – This contains the **aggregate score** calculated in the off-chain oracle. Due to its length this variable is stored as a string
- ``_off_chain`` – This contains the location of the cloud database (in this instance Cloud Firestore) JSON file of all the **individual scores** used in the aggregation with its transaction hash

This contract also contains the functions ``get_on_chain`` and ``get_off_chain`` which retrieve the aggregate score stored on-chain and cloud database URL respectively.
The address for the deployed oracle smart contract must be entered for the variable ``gateway_address``. 

