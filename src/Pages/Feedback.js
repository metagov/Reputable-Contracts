/* eslint-disable react-hooks/exhaustive-deps */
import React from "react";
import { useLocation } from "react-router-dom";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom";
//mport Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { Form } from "react-bootstrap";

// Get mnemonic phrase and Infura API key from environment variables
const mnemonicPhrase = process.env.REACT_APP_MNEMONIC_PHRASE;
const sepolia = process.env.REACT_APP_SEPOLIA;

const { ethers } = require("ethers");
const provider = new ethers.providers.JsonRpcProvider(sepolia);
const wallet = ethers.Wallet.fromMnemonic(mnemonicPhrase);
const account = wallet.connect(provider);
console.log(account.address);

/**  <h2>User ID:{userID} </h2>
      <h2>Campaign ID:{campaignID} </h2>
      <h2>Token:{token} </h2> */
const Feedback = () => {
  const location = useLocation();
  const storeName = location.state?.fromDashboard;
  console.log(storeName);
  // const userName = "Rashmi";
  const history = useHistory();
  const [open, setOpen] = React.useState(false);
  const [tokenUsedModal, setTokenUsedModal] = React.useState(false);
  const { userID, sellerID, campaignID, tokenID } = useParams();
  const [sName, setSName] = React.useState("");
  const web_address = "0xDafdC2Ae8ceEB8c4F70c8010Bcd7aD6853CeF532";
  const oracle_address = "0x42F7Cf57BD6C0C8d92EBb3F1Ca4166E1A6c4229B";

  let MyContract = require("../abi/WebInterface.json");


  const OracleContractABI = require("../abi/OracleInterface.json");

  const contract = new ethers.Contract(web_address, MyContract.abi, account);

  const OracleContract = new ethers.Contract(
    oracle_address,
    OracleContractABI.abi,
    account
  );

  const yesClicked = () => {
    console.log("Print userID is " + userID);
    console.log("Print seller ID is " + sellerID);
    console.log("Print tokenID is " + tokenID);
    console.log("Print campaignID is " + campaignID);
    // console.log("ashdahsdasd" + JSON.stringify(props.color));

    //setOpen(true);
    //setOpen(true);
    //call setOracleAddress()
    //import Web3 from "web3";

    const init = async () => {
      const result = await contract.getSellerId();
      const parsed_sellerID = parseInt(sellerID);
      const parsed_tokenID = parseInt(tokenID);
      const parsed_userID = parseInt(userID);
      const used = await contract.isUsed(parsed_sellerID, parsed_tokenID);
      //await contract.setOracleAddress(oracle_address);
      const transactionData = contract.interface.encodeFunctionData("adder", [
        parsed_sellerID,
        parsed_tokenID,
        parsed_userID,
        1,
      ]);
      const gasLimit = await contract.estimateGas.adder(
        parsed_sellerID,
        parsed_tokenID,
        parsed_userID,
        1
      );
      const nonce = await provider.getTransactionCount(wallet.address);


      const transaction = {
        to: web_address,
        data: transactionData,
        gasLimit: gasLimit,
        gasPrice: ethers.utils.parseUnits("20", "gwei"),
        nonce: nonce
      };

      if (!used) {
        // Sign the transaction
        const signedTransaction = await account.signTransaction(transaction);

        // Send the transaction
        const transactionResponse = await provider.sendTransaction(
          signedTransaction
        );
        console.log("Transaction hash:", transactionResponse.hash);

        // Wait for the transaction to be mined
        const transactionReceipt = await provider.waitForTransaction(
          transactionResponse.hash
        );
        console.log("Transaction receipt:", transactionReceipt);

        console.log("result:" + result);
        console.log("isUsed:" + used);

        /*           contract.events.ScoreAdded({})//, {fromBlock:0, toBlock: 'latest'})
          .on('data', async function(event){
              console.log(event.returnValues);
              //get the data and compare the token, seller id and user id
              //enable the modal to tell the user that the score has been added
          })
          .on('error', console.error); */
        //call past events until block -100
        //then filter the user id, token and seller and if they match, the modal runs.

        //working for past events (but not the latest + 1)
        //setTimeout(() => { console.log("Waiting for event to be emitted!"); }, 2000);
        await new Promise((resolve) => setTimeout(resolve, 5500));
        const latest = await provider.getBlockNumber();
        const fromBlock = latest - 100; // Last 100 blocks
        const toBlock = latest + 1;
        console.log("Latest block number:", latest);
        const eventFilter = contract.filters.ScoreAdded(null,null, null); // Adjust the event name and arguments according to your contract

        const events = await contract.queryFilter(eventFilter, fromBlock, toBlock);
  console.log("events:" + events)
         // Manually filter events by tokenID
  const filteredEvents = events.filter((event) => {
    // Decode the event data to get the tokenID value
    const decodedData = contract.interface.parseLog(event);
    const eventTokenID = decodedData.args[2];
    
    return eventTokenID.toString() === tokenID; // Filter by the desired tokenID
  });

  console.log("Filtered events:", filteredEvents);

     
        // console.log("Logs", logs, `${logs.length} logs`);
        // for (let i = 0; i < logs.length; i++) {
        //   let j = logs[i].returnValues;
         
        //   if (
        //     j["token"] === tokenID &&
        //     j["sellerId"] === sellerID &&
        //     j["user_id"] === userID
        //   ) {
        //     console.log(
        //       "token, sellerId and user id have been added to the blockchain"
        //     );
        //     setOpen(true);

        //     break;
        //   }
        // }
      } else {
        setTokenUsedModal(true);
        console.log("token is already used/not valid!");
        //call the modal to tell the user that the token has already been used or not valid.
      }
    };
    init();
  };

  React.useEffect(() => {
    console.log("componentDidMount");
    if (sellerID === "11") {
      setSName("Tesco");
    } else if (sellerID === "12") {
      setSName("Asda");
    } else if (sellerID === "13") {
      setSName("Sainsbury");
    }

    contract
      .on("ScoreAdded", function (event) {
        console.log("ScoreAdded event emitted:", event.returnValues);
        // Perform actions when the event is emitted
      })
      .on("error", console.error);

    OracleContract.on("RequestScoreEvent", function (event) {
      console.log("RequestScore event emitted:", event.returnValues);
      // Perform actions when the event is emitted
    }).on("error", console.error);
  }, [OracleContract, contract, sellerID]);

  // No button function
  const noClicked = () => {
    console.log("Nooooo");
    //setOpen(true);

    const initNo = async () => {
      //const result = await contract.methods.getData(1).call();
      //getSellerId ()
      //personal account
      //web3.eth.defaultAccount = web3.eth.accounts[0];
      const result = await contract.getSellerId();
      const parsed_sellerID = parseInt(sellerID);
      const parsed_tokenID = parseInt(tokenID);
      const parsed_userID = parseInt(userID);
      const used = await contract.isUsed(parsed_sellerID, parsed_tokenID);

      const transactionData = contract.interface.encodeFunctionData("adder", [
        parsed_sellerID,
        parsed_tokenID,
        parsed_userID,
        0,
      ]);
      const gasLimit = await contract.estimateGas.adder(
        parsed_sellerID,
        parsed_tokenID,
        parsed_userID,
        0
      );
      const nonce = await provider.getTransactionCount(wallet.address);

      const transaction = {
        to: web_address,
        data: transactionData,
        gasLimit: gasLimit,
        gasPrice: ethers.utils.parseUnits("20", "gwei"),
        nonce: nonce
      };

      if (!used) {
        //contract.methods.adder(parsed_sellerID, parsed_tokenID, parsed_userID, 0).send({from:address});//{from: '0x3dec0B5699F4511c133d9d9482B81Ac64A3Ef6eA'});
        // Sign the transaction
        const signedTransaction = await account.signTransaction(transaction);

        // Send the transaction
        const transactionResponse = await provider.sendTransaction(
          signedTransaction
        );
        console.log("Transaction hash:", transactionResponse.hash);

        // Wait for the transaction to be mined
        const transactionReceipt = await provider.waitForTransaction(
          transactionResponse.hash
        );
        console.log("Transaction receipt:", transactionReceipt);

        console.log(result);
        /*           contract.events.ScoreAdded({})//, {fromBlock:0, toBlock: 'latest'})
          .on('data', async function(event){
              console.log(event.returnValues);
              //get the data and compare the token, seller id and user id
              //enable the modal to tell the user that the score has been added
          })
          .on('error', console.error); */
        //call past events until block -100
        //then filter the user id, token and seller and if they match, the modal runs.

        //working for past events (but not the latest + 1)
        //setTimeout(() => { console.log("Waiting for event to be emitted!"); }, 2000);
        await new Promise((resolve) => setTimeout(resolve, 3500));
        const latest = await provider.getBlockNumber();
        const fromBlock = latest - 10; // Last 100 blocks
        const toBlock = latest + 1;
        console.log("Latest block number:", latest);
        const eventFilter = contract.filters.ScoreAdded(null, null, null); // Adjust the event name and arguments according to your contract
        const events = await contract.queryFilter(eventFilter, fromBlock, toBlock);
        const filteredEvents = events.filter((event) => {
          // Decode the event data to get the tokenID value
          const decodedData = contract.interface.parseLog(event);
          const eventTokenID = decodedData.args[2];
          
          return eventTokenID.toString() === tokenID; // Filter by the desired tokenID
        });
      
        console.log("Filtered events:", filteredEvents);
        //console.log("Latest block: ", latest);

        // const logs = await contract.getPastEvents("ScoreAdded", {
        //   fromBlock: latest - 10, //could be last 100 blocks
        //   toBlock: latest + 1,
        //   filter: { token: tokenID },
        //   //filter: { token: tokenID, user_id: userID, sellerId: sellerID}
        // });
        
        // console.log("Logs", logs, `${logs.length} logs`);
        // for (let i = 0; i < logs.length; i++) {
        //   let j = logs[i].returnValues;
        //   //if (j['Result'])
        //   //console.log("J value: ", j[0]);
        //   //console.log("J value token: ", j['token']);
        //   //console.log("TokenID: ", tokenID);
        //   if (
        //     j["token"] === tokenID &&
        //     j["sellerId"] === sellerID &&
        //     j["user_id"] === userID
        //   ) {
        //     console.log(
        //       "token, sellerId and user id have been added to the blockchain"
        //     );
        //     //modal insertion
        //     setOpen(true);
        //     //showModal();

        //     break;
        //   }
        // }
      } else {
        setTokenUsedModal(true);
        console.log("token is already used/not valid!");
        //call the modal to tell the user that the token has already been used or not valid.
      }
    };
    initNo();
  };
  //Close the Model
  const handleClose = () => {
    setOpen(false);
    history.goBack();
    window.close();
  };
  const handleModalClose = () => {
    setTokenUsedModal(false);
    //history.goBack();
    window.close();
  };
  //UI

  return (
    <div className="d-flex justify-content-center mb-3 shadow p-3 ">
      <Form style={{ position: "absolute", top: "40%" }}>
        {/** 
        <Row>
          <Col>
            <Form.Control placeholder={userID} readOnly />
          </Col>
          <Col>
            <Form.Control
              placeholder={sellerID}
              onChange={(e) => setSellerID(e.target.value)}
            />
          </Col>
          <Col>
            <Form.Control
              placeholder={tokenID}
              onChange={(e) => setToken(e.target.value)}
            />
          </Col>
          <Col>
            <Form.Control
              placeholder={campaignID}
              onChange={(e) => setCmpID(e.target.value)}
            />
          </Col>
        </Row>
        */}
        <div
          className="d-flex justify-content-center"
          style={{
            paddingTop: 30,
          }}
        >
          <h3> Are you satisfied with the service delivered by {sName}?</h3>
        </div>
        <div className="d-flex justify-content-center btn-toolbar ">
          <div
            style={{
              paddingRight: 20,
            }}
          >
            <Button variant="primary" onClick={yesClicked}>
              Yes
            </Button>
          </div>
          <div>
            <Button variant="danger" onClick={noClicked}>
              NO
            </Button>
          </div>
        </div>
      </Form>
      <Modal isOpen={open}>
        <ModalHeader>Confirmation</ModalHeader>
        <ModalBody>
          <br />
          Your rating has successfully been submitted.
        </ModalBody>
        <ModalFooter>
          <Button onClick={handleClose} variant="primary">
            Close
          </Button>
        </ModalFooter>
      </Modal>

      <Modal isOpen={tokenUsedModal}>
        <ModalHeader>Notice</ModalHeader>
        <ModalBody>
          <br />
          The token is not valid.
        </ModalBody>
        <ModalFooter>
          <Button onClick={handleModalClose} variant="primary">
            Close
          </Button>
        </ModalFooter>
      </Modal>
      {/* <Modal isOpen={open}>
        <ModalHeader>The Fruit Shop</ModalHeader>
        <ModalBody>
          Hi {userName},<br />
          <br />
          We're always working to improve our services, your feedback is
          valuable and it will help us to decide what improvements should be
          made.
        </ModalBody>
        <ModalFooter>
          <Button onClick={handleClose} variant="primary">
            Close
          </Button>
        </ModalFooter>
      </Modal> */}
    </div>
  );
};

export default Feedback;
