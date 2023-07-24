import React, { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import { Col, Row, Form } from "react-bootstrap";
//import * as ReactBootStrap from "react-bootstrap";
import database from "../firebase.config";
import { collection, query, getDocs } from "firebase/firestore";
//import "bootstrap/dist/css/bootstrap.min.css";
//import { NeuButton } from "neumorphism-react";
import { Select, MenuItem, FormControl, InputLabel } from "@material-ui/core";
//import axios from "axios";
import { makeStyles } from "@material-ui/styles";
import { color } from "@material-ui/system";
import { async } from "@firebase/util";

const useStyles = makeStyles((theme) => ({
  formControl: {
    width: 150,
  },
}));
//TODO: add try catch blocks to this page to handle rejections and exceptions
//TODO: Create new user ID for every new session of app
const Dashboard = () => {
  const [showResults, setShowResults] = React.useState(false);
  const [showResIndi, setShowResultsIndi] = React.useState(false);
  const [showResSeller, setShowResultsSeller] = React.useState(false);
  const [showVerifiedReputResults, setShowVerifiedRepResults] =
    React.useState(false);
  const [showVerifiedIndResults, setShowVerifiedIndResults] =
    React.useState(false);

  const onClickRepVeryify = () => setShowVerifiedRepResults(true);
  const onClickIndVeryify = () => setShowVerifiedIndResults(true);

  const classes = useStyles();
  const [showVeriyButton, setShowVerifyButton] = React.useState(false);

  const [value, setvalue] = useState("");
  const [value1, setValue1] = useState("");

  const [value0Error, setValue0Err] = useState({});
  const [value1Error, setValue1error] = useState({});

  const [placeHolder, setPlaceHolder] = useState("Seller ID / User ID");

  const [newdata, setnewData] = React.useState([{}]);
  const [indivScore, setIndiviScore] = React.useState([]);
  const [sellerScore, setSellerScore] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const [sellerID, setSellerID] = React.useState([]);

  // Var's used to get and set data.
  const [sellerTxhash, setsellerTxhash] = React.useState([]);
  const [timestamp, setTimeStamp] = React.useState([]);
  const [rep_score, setRepScore] = React.useState();
  const [verifyRepScore, setVerifyRepScore] = React.useState();
  const [isRendered, setisRendered] = React.useState(false);

  //use this to store set total rep score:
  const [score, setScore] = React.useState([]);

  const VerifyRepResults = () => (
    <div>
      <h5> Reputation score: {verifyRepScore}</h5>
      <h5>Tx_Hash: {sellerTxhash}</h5>
      <h5>Time Stamp: {timestamp} </h5>
    </div>
  );
  const VerifyIndResults = () => <h1>Some Verified Rep Results</h1>;

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    //let userID = 1235;
    let dbRef = query(collection(database, "individual_scores"));
    const dataRef = await getDocs(dbRef)
      .then((snapshot) => {
        if (snapshot.empty) {
          console.log("No matching User ID");
          return;
        }

        snapshot.forEach((doc) => {
          console.log(doc.id, "=>", doc.data());
          const data = doc.data()["data"];

          setnewData(data);
          // console.log("here", newdata.length);
          // console.log(newdata[5]);
        });
      })
      .catch((err) => {
        console.log("Error getting documents", err);
      });
  };

  const ReputationalResults = () => (
    <div>
      <div className=" d-flex justify-content-center mb-3 ">
        <h3>Reputation Score: {score}</h3>
      </div>
      <div style={{ position: "absolute" }}>
        <Button variant="primary" onClick={onClickRepVeryify}>
          Verify Score
        </Button>
      </div>
    </div>
  );

  const IndividualScore = () => (
    <div>
      <div className=" d-flex justify-content-center mb-3 ">
        <h1>Individual Score </h1>
      </div>
      <div style={{ position: "absolute" }}>
        <p style={{ marginLeft: -490 }}>{indivScore}</p>
      </div>
    </div>
  );
  
  const t0 = performance.now();
  const getSellerScore = async (sellerId) => {
    console.log("Assign clicked");
    //alert("You clicked assign");
    const getIndScore = await fetch("https://reputable-swagger-api.onrender.com/reputation_score", {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify({ sellerId: sellerId }),
    }).then((response) =>
      response.json().then((data) => {
        console.log("here", data["score"]); //remove log and setData to data
        //console.log()
        setScore(data["score"]);
      })
    );
    const t1 = performance.now();
    console.log(`Time taken for seller score: ${t1-t0} ms`);
    //await new Promise(resolve => setTimeout(resolve, 3000));
    //Fetch Needed to be called with seller id and set response
    //Get the data  from fetch and store it in a variable and then just show
    const t2 = performance.now();
    fetch("https://reputable-swagger-api.onrender.com/verify_reputation?sellerId=" + sellerId, {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      //body: JSON.stringify({ sellerId: sellerId }),
    }).then((response) =>
      response.json().then((data) => {
        setsellerTxhash(data["hash"]);
        setTimeStamp(data["timestamp"]); //remove log and setData to data
        setVerifyRepScore(data["score"]);
        //console.log()
      })
    );
    const t3 = performance.now();
    console.log(`Time taken for verifyseller score: ${t3-t2} ms`);
    //setScore(sellerId);
    // try {
    //   const data = await axios
    //     .get("https://api.lyrics.ovh/v1/Eminem/Godzilla")
    //     .then((res) => {
    //       console.log("asdasd", res);
    //       setScore(res.data.lyrics);
    //     });
    //   setLoading(true);
    // } catch (e) {
    //   console.log(e);
    // }
  };

  const onChangeOption = (e) => {
    setShowResults(false);
    setShowResultsIndi(false);
    setShowResultsSeller(false);
    setValue1("");
    setShowVerifiedRepResults(false);
    setShowVerifiedIndResults(false);

    if (e === "Reputational Score") {
      setPlaceHolder("Seller ID");
    } else if (e === "Individual Score") {
      setPlaceHolder("User ID");
    }
  };
  const custom_sort = (a, b) => {
    return new Date(a.timeStamp).getTime() - new Date(b.timeStamp).getTime();
  };

  const onSubmit = async (e) => {
    e.preventDefault();

    const isValid = formValidation();

    //Call firestore get data here
    var val = parseInt(value1);

    if (isValid) {
      // setTimeout(getSellerScore(val), 3000);
      if (value === "Reputational Score") {
        console.log("JSON data", newdata);
        console.log("Running Reputational score");
        // let arrayofIndividualScores = [];
        try {
          await getSellerScore(val);
          // const findUserData = newdata.find((ui) => ui.seller_id === val);
          //  console.log(findUserData["individual_score"]);
          //  setsellerTxhash(findUserData["tx_hash"]);
          //  setTimeStamp(findUserData["Timestamp"]);
          // newdata.map((i) => {
          //   if (i.seller_id === val) {
          //     //console.log("Seller ID: ", i.seller_id, val);
          //     // console.log("Individual Score", i.individual_score);
          //     arrayofIndividualScores.push(i.individual_score);
          //     // setSellerID(i.sellerID);
          //   }
          // });
          //The array ready to push into API
          //console.log(arrayofIndividualScores);
          // console.log("asdasda" + val);
          //Get the score and display it here here from the api call..
          // Do the API CALLS
          // fetch("http://localhost:5000/reputation_score", {
          //   method: "POST",
          //   mode: "cors",
          //   cache: "no-cache",
          //   credentials: "same-origin",
          //   headers: {
          //     Accept: "application/json",
          //     "Content-Type": "application/json",
          //   },
          //   redirect: "follow",
          //   referrerPolicy: "no-referrer",
          //   body: JSON.stringify({ sellerId: val }),
          // }).then((response) =>
          //   response.json().then((data) => {
          //     console.log("here", data["score"]); //remove log and setData to data
          //     //console.log()
          //     setScore(data["score"]);
          //   })
          // );
          //await new Promise(resolve => setTimeout(resolve, 3000));
          //Fetch Needed to be called with seller id and set response
          //Get the data  from fetch and store it in a variable and then just show
          // fetch("http://localhost:5000/verify_reputation?sellerId=" + val, {
          //   method: "GET",
          //   mode: "cors",
          //   cache: "no-cache",
          //   credentials: "same-origin",
          //   headers: {
          //     Accept: "application/json",
          //     "Content-Type": "application/json",
          //   },
          //   redirect: "follow",
          //   referrerPolicy: "no-referrer",
          //   //body: JSON.stringify({ sellerId: sellerId }),
          // }).then((response) =>
          //   response.json().then((data) => {
          //     setsellerTxhash(data["hash"]);
          //     setTimeStamp(data["timestamp"]); //remove log and setData to data
          //     setVerifyRepScore(data["score"]);
          //     //console.log()
          //})
          //);
          // findUserData = newdata.find((ui) => ui.seller_id === 123);
          //setIndiviScore("adasdas", findUserData["individual_score"]);
          // Do Api calls here
          console.log("SCOREHERE",score)
        } catch (e) {
          //setShowResultsSeller(true);
          setScore(
            <h6 style={{ color: "red" }}>
              Unable to find Seller ID: {value1}
            </h6>
          );

          //setShowResultsSeller(true);
          //setShowVerifiedRepResults(true);
        }
        setShowResultsSeller(true);

        // //Run reputatioal score result
        //
        //   console.log("asdasdasd", sellerTxhash);
        // }

        // setShowResults(true);
      } else if (value === "Individual Score") {
        // Run indivisual score result
        var t4 = performance.now();
        console.log("Running Individual score fun ");
        try {
          const findUserData = newdata.find((ui) => ui.user_id === val);
          console.log(findUserData["individual_score"]);
          setIndiviScore(findUserData["individual_score"]);
        } catch (e) {
          setIndiviScore(
            <h6 style={{ color: "red", marginLeft: 490 }}>
              Unable To Find Score For The User ID {value1}
            </h6>
          );
        }

        setShowResultsIndi(true);
      }
      const t5 = performance.now();
      console.log(`Individual score took ${t5 - t4} milliseconds.`);
    }
  };

  const formValidation = () => {
    const optionErr = {};
    const secondInputErr = {};

    let isValid = true;

    if (value === "") {
      optionErr.optionEmpty = "Please choose an Option";
      console.log(optionErr);
      isValid = false;
    }
    if (value1 === "") {
      secondInputErr.optionEmpty = "Please Type in an Seller ID / User ID";
      isValid = false;
    }

    setValue0Err(optionErr);
    setValue1error(secondInputErr);

    return isValid;
  };

  return (
    <div className="d-flex justify-content-center mb-3 shadow p-3 ">
      {Object.keys(value0Error).map((key) => {
        return (
          <div
            style={{
              fontWeight: "bold",
              color: "red",
              position: "absolute",
              top: "25%",
            }}
            className="d-flex justify-content-center"
          >
            {" "}
            {value0Error[key]}
          </div>
        );
      })}
      {Object.keys(value1Error).map((key) => {
        return (
          <div
            style={{
              fontWeight: "bold",
              color: "red",
              position: "absolute",
              top: "29%",
            }}
            className="d-flex justify-content-center"
          >
            {" "}
            {value1Error[key]}
          </div>
        );
      })}

      <Form style={{ position: "absolute", top: "40%" }} onSubmit={onSubmit}>
        <Row>
          <Col>
            <FormControl className={classes.formControl}>
              <InputLabel>Choose Query</InputLabel>
              <Select
                id="select_option"
                style={{ width: 300 }}
                //onChange={(e) => {setvalue(e.target.value)}
                onChange={(e) => {
                  setvalue(e.target.value);
                  onChangeOption(e.target.value);
                }}
              >
                <MenuItem value={"Reputational Score"}>
                  Seller Reputation Score
                </MenuItem>
                <MenuItem value={"Individual Score"}>
                  Check Individual User Feedback
                </MenuItem>
              </Select>
            </FormControl>
          </Col>
          <Col style={{ paddingLeft: 160 }}>
            <Form.Control
              type="number"
              pattern="^-?[0-9]\d*\.?\d*$"
              style={{ width: 200, height: 55 }}
              placeholder={placeHolder}
              onChange={(e) => setValue1(e.target.value)}
            />
          </Col>

          <Col>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Col>
        </Row>
        <div
          className="d-flex justify-content-center"
          style={{
            paddingTop: 30,
          }}
        >
          {showResSeller ? <ReputationalResults /> : null}
        </div>
        <div
          className="d-flex justify-content-center"
          style={{
            paddingTop: 30,
          }}
        >
          {showResIndi ? <IndividualScore /> : null}
        </div>

        <div className="d-flex justify-content-center btn-toolbar ">
          <div
            style={{
              paddingRight: 20,
              paddingTop: 20,
            }}
          ></div>
        </div>

        <div
          className="d-flex justify-content-center"
          style={{
            paddingTop: 30,
          }}
        >
          {showVerifiedReputResults ? <VerifyRepResults /> : null}
        </div>
        <div
          className="d-flex justify-content-center"
          style={{
            paddingTop: 30,
          }}
        >
          {showVerifiedIndResults ? <VerifyIndResults /> : null}
        </div>
      </Form>
    </div>
  );
};

export default Dashboard;
