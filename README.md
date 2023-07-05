# Test 1ST UI React JS

=)


## Installation
```bash
npm start
```

## Usage
```
http://localhost:3000/feedback/S16120405/SellerID123/TK1996/CMP21/

```

## Requirments
![](images/img1.PNG)

## Output

![](images/img2.PNG)


## Intructions to run

Clone REPUTABLE Repo

```
git clone git@github.com:thelastjosh/REPUTABLE.git
```

The below instructions to run the project are derived from this document
https://github.com/thelastjosh/REPUTABLE/blob/prince/ONTOCHAIN_D4_REPUTABLE_VF.pdf

Please make sure to clone the `test-dev-rashmi` branch
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
`ganache-cli `

(Terminal 3):
```
truffle compile
truffle migrate --network development
```

after compiling and deploying the contracts,
please update the contract addresses for each smart contract in the src/Pages/Feedback.js and .env file

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





