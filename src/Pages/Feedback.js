import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom";
//mport Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { Col, Row, Form } from "react-bootstrap";
import dotenv from  'dotenv'

/**  <h2>User ID:{userID} </h2>
      <h2>Campaign ID:{campaignID} </h2>
      <h2>Token:{token} </h2> */
const Feedback = () => {
  const location = useLocation();
  const storeName = location.state?.fromDashboard;
  console.log(storeName);
  const userName = "Rashmi";
  const history = useHistory();
  const [open, setOpen] = React.useState(false);
  const [tokenUsedModal, setTokenUsedModal] = React.useState(false);
  const { userID, sellerID, campaignID, tokenID } = useParams();
  const [sName, setSName] = React.useState("");
  const address = '0x4C0bAD2960fDbC71D5177D0458Ea8691c4C0E773';
  const web_address = '0xEe82922233B5f4Db3E696846b0a2B23dDe7d4F9f';
const oracle_address = '0x144f2012307CE07494ed3764FC804819799b649c';
//   const address = process.env.ADDRESS;
// const web_address = process.env.WEB_ADDRESS;

/*   const showModal = () => {
    return( */
      
/*         )
  } */
  const Web3 = require('web3');

  const web3 = new Web3('http://localhost:8545');
  const MyContract = require('../abi/WebInterface.json');
  const OracleContractABI = require('../abi/OracleInterface.json')

  const contract =  new web3.eth.Contract(
    MyContract.abi,
    //deployedNetwork.address
    web_address
    );

    const OracleContract = new web3.eth.Contract(
      OracleContractABI.abi,
      oracle_address
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
    
      const id = await web3.eth.net.getId();
      console.log("ID:"+id)
      const deployedNetwork = MyContract.networks[id];
      //const web_address = '0x30e32a2Ace7225Ef840658eB0E68743E9E34539C';
       
  
        //const result = await contract.methods.getData(1).call();
        //getSellerId ()
        //personal account

        const result = await contract.methods.getSellerId().call();
        const parsed_sellerID = parseInt(sellerID);
        const parsed_tokenID = parseInt(tokenID);
        const parsed_userID = parseInt(userID);
        const used = await contract.methods.isUsed(parsed_sellerID, parsed_tokenID).call();
       await contract.methods.setOracleAddress(oracle_address).call();

        if (!used){
          contract.methods.adder(parsed_sellerID, parsed_tokenID, parsed_userID, 1).send({from:address});//{from: '0x3dec0B5699F4511c133d9d9482B81Ac64A3Ef6eA'});
          console.log("result:"+ result);
          console.log("isUsed:"+ used);

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
          await new Promise(resolve => setTimeout(resolve, 5500));
          const latest = await web3.eth.getBlockNumber();
          //console.log("Latest block: ", latest);

          const logs = await contract.getPastEvents("ScoreAdded", {
            fromBlock: latest -10, //could be last 100 blocks
            toBlock: latest+1,
            filter: { token: tokenID}
            //filter: { token: tokenID, user_id: userID, sellerId: sellerID}
          });
          console.log("Logs", logs, `${logs.length} logs`);
          for (let i = 0; i < logs.length; i++) {
            let j = logs[i].returnValues;
            //if (j['Result'])
            //console.log("J value: ", j[0]);
            //console.log("J value token: ", j['token']);
            //console.log("TokenID: ", tokenID);
            if (j['token'] == tokenID && j['sellerId'] == sellerID && j['user_id'] == userID){
              console.log("token, sellerId and user id have been added to the blockchain");
              //modal insertion
              setOpen(true);
              //showModal();
              
              break;
            }
          }      
        }
        else{
          setTokenUsedModal(true);
          console.log("token is already used/not valid!")
          //call the modal to tell the user that the token has already been used or not valid.
        }

        
    }
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

    const eventListener = contract.events.ScoreAdded({})
    .on('data', function(event) {
      console.log('ScoreAdded event emitted:', event.returnValues);
      // Perform actions when the event is emitted
    })
    .on('error', console.error);

    const eventListenerOracle = OracleContract.events.RequestScoreEvent({})
    .on('data', function(event) {
      console.log('RequestScore event emitted:', event.returnValues);
      // Perform actions when the event is emitted
    })
    .on('error', console.error);

    return () => {
      eventListener.unsubscribe();
      eventListenerOracle.unsubscribe();
    };
  }, []);

  // No button function
  const noClicked = () => {
    console.log("Nooooo");
    //setOpen(true);
    const Web3 = require('web3');
    
  
    const MyContract = require('../abi/WebInterface.json');
    
    const initNo = async () => {
      const web3 = new Web3('http://localhost:8545');
    
      const id = await web3.eth.net.getId();
      const deployedNetwork = MyContract.networks[id];
      //const web_address = '0x00f16331A8FB584C5442E929cBEA251471c61ABd';
      const contract = new web3.eth.Contract(
        MyContract.abi,
        //deployedNetwork.address
        web_address
        );
    
        //const result = await contract.methods.getData(1).call();
        //getSellerId ()
        //personal account
        //web3.eth.defaultAccount = web3.eth.accounts[0];
        const result = await contract.methods.getSellerId().call();
        const parsed_sellerID = parseInt(sellerID);
        const parsed_tokenID = parseInt(tokenID);
        const parsed_userID = parseInt(userID);
        const used = await contract.methods.isUsed(parsed_sellerID, parsed_tokenID).call();
        if (!used){
          contract.methods.adder(parsed_sellerID, parsed_tokenID, parsed_userID, 0).send({from:address});//{from: '0x3dec0B5699F4511c133d9d9482B81Ac64A3Ef6eA'});
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
          await new Promise(resolve => setTimeout(resolve, 3500));
          const latest = await web3.eth.getBlockNumber();
          //console.log("Latest block: ", latest);

          const logs = await contract.getPastEvents("ScoreAdded", {
            fromBlock: latest -10, //could be last 100 blocks
            toBlock: latest+1,
            filter: { token: tokenID}
            //filter: { token: tokenID, user_id: userID, sellerId: sellerID}
          });
          console.log("Logs", logs, `${logs.length} logs`);
          for (let i = 0; i < logs.length; i++) {
            let j = logs[i].returnValues;
            //if (j['Result'])
            //console.log("J value: ", j[0]);
            //console.log("J value token: ", j['token']);
            //console.log("TokenID: ", tokenID);
            if (j['token'] == tokenID && j['sellerId'] == sellerID && j['user_id'] == userID){
              console.log("token, sellerId and user id have been added to the blockchain");
              //modal insertion
              setOpen(true);
              //showModal();
              
              break;
            }
          }      
        }
        else{
          setTokenUsedModal(true);
          console.log("token is already used/not valid!")
          //call the modal to tell the user that the token has already been used or not valid.
        }

        
    }
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
