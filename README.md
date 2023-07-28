# Reputable Smart Contracts with Demo App

## Intructions to run

Clone REPUTABLE Repo

```
git clone git@github.com:thelastjosh/REPUTABLE.git
```

The below instructions to run the project are derived from this document
https://github.com/thelastjosh/REPUTABLE/blob/prince/ONTOCHAIN_D4_REPUTABLE_VF.pdf

Please make sure to clone the `with-rpc` branch
and also you are using Node v16, if not
```
nvm use 16
```


(Terminal 1):
```
pip install -r requirements.txt
npm install
```

(Terminal 2):
```
truffle compile
truffle migrate --network development
```

after compiling and deploying the contracts,
please update the contract addresses for each smart contract in the `src/Pages/Feedback.js` and `.env` file

now please run 
`python3 setOracle.py `

a successful transaction should look like this
![](https://hackmd.io/_uploads/HkP5Z4ft2.png)


(Terminal 1):
`npm run start`

(Terminal 4):
`python3 oracle2.py`

(Terminal 5):
`python3 ./swagger/swaggerAPI.py`

Note: This is an input data document that the script uses
https://firestore.googleapis.com/v1/projects/reputable-b7df1/databases/(default)/documents/individual_scores/mjHPrqCFPf8y3vAJ9vE1

https://hackmd.io/MC_QqPFTQTe3b1d5bUg62g

# REPUTABLE Smart Contracts deployment
#### Helpful links
https://ontochain.ngi.eu/content/reputable-provenance-aware-decentralized-reputation-system-blockchain-based-ecosystems

https://www.researchgate.net/publication/356890067_A_New_Blockchain_Ecosystem_for_Trusted_Traceable_and_Transparent_Ontological_Knowledge_Management_Position_Paper

## Deployed Smart Contract Addresses
### Sepolia

### OnChainReputationData.sol :  
`0x206e22fD482ae75306FF1869E852A3D9Ae48FE76`
https://sepolia.etherscan.io/address/0x206e22fD482ae75306FF1869E852A3D9Ae48FE76#code

### DataService.sol : 
`0xfEb6Cf237c031a2d6c97E8E415064A3d1126232A` 
https://sepolia.etherscan.io/address/0xfEb6Cf237c031a2d6c97E8E415064A3d1126232A#code

### Gateway.sol : 
`0xe402996DEea7a76bfB4FB0BdC648802952840207`
https://sepolia.etherscan.io/address/0xe402996DEea7a76bfB4FB0BdC648802952840207#code

### Oracle.sol : 
`0x13441a7B32E4D012a657Bc0794Fb9BF5717f186F`
https://sepolia.etherscan.io/address/0x13441a7B32E4D012a657Bc0794Fb9BF5717f186F#code


### Goreli

### OnChainReputationData.sol

`0xf2f8b941E18693c1Dc431c93613f8DdD63D02ac8`
https://goerli.etherscan.io/address/0xf2f8b941E18693c1Dc431c93613f8DdD63D02ac8#code

### DataService.sol aka WebInterface
`0xDafdC2Ae8ceEB8c4F70c8010Bcd7aD6853CeF532`
https://goerli.etherscan.io/address/0xdafdc2ae8ceeb8c4f70c8010bcd7ad6853cef532#code
### Gateway.sol
`0x99442e120937Ae5c4cC3F73F3094efc97b0cf5ee`
https://goerli.etherscan.io/address/0x99442e120937Ae5c4cC3F73F3094efc97b0cf5ee#code

### Oracle.sol

`0x42F7Cf57BD6C0C8d92EBb3F1Ca4166E1A6c4229B`
https://goerli.etherscan.io/address/0x42F7Cf57BD6C0C8d92EBb3F1Ca4166E1A6c4229B#code

**Note:**
Oracle address has been set for Goreli Contract, no need to call setOracle.py when using Goreli contracts
https://goerli.etherscan.io/tx/0xc854fad7312f192bd3f237c1f59adbf5676b511fda12e9fc07c9ebc924c416cd

# Smart contract function documentation

## **Oracle.sol**

### Functions

#### `requestValue(uint _sellerId, uint[] memory _userId, string[] memory _array)`

Interacts with the Gateway contract to request a value.

**Parameters:**

- `_sellerId` (uint): The ID of the seller.
- `_userId` (uint[]): An array of user IDs.
- `_array` (string[]): An array of values.

**Usage Example:**

```solidity
uint sellerId = 123;
uint[] memory userIds = [1, 2, 3];
string[] memory values = ["value1", "value2", "value3"];

oracle.requestValue(sellerId, userIds, values);
```

#### `requestScore(uint _sellerId, uint token_val, uint user_id, uint _indi_score)`

Requests a score for a seller from the Oracle backend.

**Parameters:**

- `_sellerId` (uint): The ID of the seller.
- `token_val` (uint): The token value.
- `user_id` (uint): The user ID.
- `_indi_score` (uint): The individual score.

**Usage Example:**

```solidity
uint sellerId = 123;
uint tokenValue = 456;
uint userId = 789;
uint individualScore = 90;

oracle.requestScore(sellerId, tokenValue, userId, individualScore);
```

#### `returnToGateway(address _gateway_address, string memory _aggr_score, string memory _off_chain)`

Returns the aggregated score to the Gateway contract.

**Parameters:**

- `_gateway_address` (address): The address of the Gateway contract.
- `_aggr_score` (string): The aggregated score.
- `_off_chain` (string): Off-chain data associated with the aggregated score.

**Usage Example:**

```solidity
address gatewayAddress = 0x1234567890123456789012345678901234567890;
string memory aggregatedScore = "85";
string memory offChainData = "Additional information";

oracle.returnToGateway(gatewayAddress, aggregatedScore, offChainData);
```

**Events**

#### `RequestValueEvent(uint sellerId, uint[] userId, string[] array)`

Emitted when a value is requested from the Oracle backend.

**Parameters:**

- `sellerId` (uint): The ID of the seller.
- `userId` (uint[]): An array of user IDs.
- `array` (string[]): An array of values.

#### `RequestScoreEvent(uint sellerId, uint token_val, uint user_id, uint indi_score)`

Emitted when a score is requested for a seller.

**Parameters:**

- `sellerId` (uint): The ID of the seller.
- `token_val` (uint): The token value.
- `user_id` (uint): The user ID.
- `indi_score` (uint): The individual score.

---

## **DataService.sol**

### Functions

#### `setOracleAddress(address _oracle_address)`

Sets the address of the Oracle contract.

**Important: You would need to call this function once after deploying Oracle smart contract**

**Parameters:**

- `_oracle_address` (address): The address of the Oracle contract.

**Usage Example:**

```solidity
address oracleAddress = 0x1234567890123456789012345678901234567890;

web.setOracleAddress(oracleAddress);
```

#### `aggr(uint _seller_id)`

Requests aggregation of scores for a specific seller from the Oracle contract.

**Parameters:**

- `_seller_id` (uint): The ID of the seller.

**Usage Example:**

```solidity
uint sellerId = 123;

web.aggr(sellerId);
```

#### `adder(uint _seller_id, uint _token_val, uint _user_id, uint _val)`

Requests a score for a seller from the Oracle contract.

**Parameters:**

- `_seller_id` (uint): The ID of the seller.
- `_token_val` (uint): The token value.
- `_user_id` (uint): The user ID.
- `_val` (uint): The value to be scored.

**Usage Example:**

```solidity
uint sellerId = 123;
uint tokenValue = 456;
uint userId = 789;
uint value = 42;

web.adder(sellerId, tokenValue, userId, value);
```

#### `add(uint _seller_id, uint _token_val, uint _user_id, string memory _enc_val)`

Adds token, user ID, and encrypted value for a specific seller.

**Parameters:**

- `_seller_id` (uint): The ID of the seller.
- `_token_val` (uint): The token value.
- `_user_id` (uint): The user ID.
- `_enc_val` (string): The encrypted value.

**Usage Example:**

```solidity
uint sellerId = 123;
uint tokenValue = 456;
uint userId = 789;
string memory encryptedValue = "abcde";

web.add(sellerId, tokenValue, userId, encryptedValue);
```

#### `getTokenArr()`

Returns an array of token values.

**Return Value:**

- `tokensArr` (uint[]): An array of token values.

**Usage Example:**

```solidity
WebInterface web = WebInterface(address);
uint[] memory tokenArray = web.getTokenArr();
```

#### `getData(uint _seller_id)`

Returns the token values, user IDs, and scores for a specific seller.

**Parameters:**-+
- `_seller_id` (uint): The ID of the seller.

**Return Value:**

- `token_val` (uint[]): An array of token values.
- `user_id` (uint[]): An array of user IDs.
- `scores` (string[]): An array of scores.

**Usage Example:**

```solidity

uint sellerId = 123;
(uint[] memory tokenArray, uint[] memory userIdArray, string[] memory scoreArray) = web.getData(sellerId);
```

#### `ASeller(uint _seller_id)`

Initializes the storage for a new seller.

**Parameters:**

- `_seller_id` (uint): The ID of the seller.

**Usage Example:**

```solidity
uint sellerId = 123;

web.ASeller(sellerId);
```

#### `isUsed(uint _seller_id, uint _token_val)`

Checks if a specific token value has been used for a seller.

**Parameters:**

- `_seller_id` (uint): The ID of the seller.
- `_token_val` (uint): The token value to check.

**Return Value:**

- `used` (bool): Returns true if the token value has been used; otherwise, returns false.

**Usage Example:**

```solidity
uint sellerId = 123;
uint tokenValue = 456;
bool isTokenUsed = web.isUsed(sellerId, tokenValue);
```

**Events**

#### `ScoreAdded(uint sellerId, uint token, uint user_id)`

Emitted

when a score is added for a specific seller.

**Parameters:**

- `sellerId` (uint): The ID of the seller.
- `token` (uint): The token value.
- `user_id` (uint): The user ID.


## **Gateway.sol**

### Functions

#### `get_on_chain()`

Returns the on-chain aggregated score.

**Return Value:**

- `aggr_score` (string): The on-chain aggregated score.

**Usage Example:**

```solidity
string memory onChainScore = gateway.get_on_chain();
```

#### `get_off_chain()`

Returns the off-chain data associated with the aggregated score.

**Return Value:**

- `off_chain` (string): The off-chain data.

**Usage Example:**

```solidity
string memory offChainData = gateway.get_off_chain();
```

#### `callback(string memory _aggr_score, string memory _off_chain)`

Callback function to receive the aggregated score and off-chain data from the Oracle contract.

**Parameters:**

- `_aggr_score` (string): The aggregated score.
- `_off_chain` (string): Off-chain data associated with the aggregated score.

**Usage Example:**

```solidity

string memory aggregatedScore = "85";
string memory offChainData = "Additional information";

gateway.callback(aggregatedScore, offChainData);
```


## **OnChainReputationData.sol**

### Functions

#### `add_rep_data(uint _seller_id, string memory _score)`

Adds reputation data for a specific seller.

**Parameters:**

- `_seller_id` (uint): The ID of the seller.
- `_score` (string): The reputation score.

**Usage Example:**

```solidity

uint sellerId = 123;
string memory score = "85";

reputationData.add_rep_data(sellerId, score);
```

#### `get_rep_data(uint _seller_id)`

Returns the reputation score for a specific seller.

**Parameters:**

- `_seller_id` (uint): The ID of the seller.

**Return Value:**

- `score` (string): The reputation score.

**Usage Example:**

```solidity
uint sellerId = 123;
string memory reputationScore = reputationData.get_rep_data(sellerId);
```
