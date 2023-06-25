import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
//mport Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Col, Row, Form } from "react-bootstrap";
import { Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";

const UserFreshFeedback = () => {
  const history = useHistory();
  const [open, setOpen] = React.useState(false);

  //Assing variables
  const [usrID, setUsrID] = useState();
  const [sellID, setSellerID] = useState();
  const [cmpID, setCmpID] = useState();
  const [token, setToken] = useState();

  //Checks if a value is present in the state variable
  //if not update to the original value
  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
    //  console.log("Print userID is " + usrID);
    // console.log("Print seller ID is " + sellID);
    //  console.log("Print tokenID is " + token);
    //  console.log("Print campaignID is " + cmpID);
  });

  const yesClicked = async () => {
    console.log("Print userID is " + usrID);
    console.log("Print seller ID is " + sellID);
    console.log("Print tokenID is " + token);
    console.log("Print campaignID is " + cmpID);
    setOpen(true);
  };

  // No button function
  const noClicked = () => {
    console.log("Nooooo");
    setOpen(true);
  };
  //Close the Model
  const handleClose = () => {
    setOpen(false);
    history.goBack();
  };
  //UI
  return (
    <div className="d-flex justify-content-center mb-3 shadow p-3 ">
      <Form style={{ position: "absolute", top: "40%" }}>
        <Row>
          <Col>
            <Form.Control
              placeholder={"User ID"}
              onChange={(e) => setUsrID(e.target.value)}
            />
          </Col>
          <Col>
            <Form.Control
              placeholder={"Seller ID"}
              onChange={(e) => setSellerID(e.target.value)}
            />
          </Col>
          <Col>
            <Form.Control
              placeholder={"Token"}
              onChange={(e) => setToken(e.target.value)}
            />
          </Col>
          <Col>
            <Form.Control
              placeholder={"Campaign ID"}
              onChange={(e) => setCmpID(e.target.value)}
            />
          </Col>
        </Row>
        <div
          className="d-flex justify-content-center"
          style={{
            paddingTop: 30,
          }}
        >
          <h3> Were you satisfied with the service delivered by {sellID}?</h3>
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
        <ModalHeader>Modal Title</ModalHeader>
        <ModalBody>
          Hi {usrID},<br />
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
      </Modal>
    </div>
  );
};

export default UserFreshFeedback;
