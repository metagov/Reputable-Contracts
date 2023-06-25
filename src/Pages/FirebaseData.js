import db from "../firebase.config";
import React, { useState, useEffect } from "react";
import { avatarClasses } from "@material-ui/core";

const FirebaseData = () => {
  const [newdata, setnewData] = React.useState([{}]);
  const [indivScore, setIndiviScore] = React.useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    {
      /** 
    fetch(
      "https://firestore.googleapis.com/v1/projects/reputable-168ee/databases/(default)/documents/individual_scores/uSn9nX6AHxH37QrYRWsE"
    )
      .then((response) => response.json())
      .then((response) => {
        setlists(response["fields"]["data"]["arrayValue"]["values"]);
        // console.log(response["fields"].data.arrayValue.values);
        // console.log(response);
      })
      .catch((err) => {
        console.log(err);
      });
    // console.log(
    //   "1" +
    //     JSON.stringify(
    //       lists[1]["mapValue"]["fields"]["user_id"]["integerValue"]
    //     )
    // );
    console.log("Found ID from json" + JSON.stringify(lists[3]));

    const filterScore = lists.filter(
      (list) =>
        list["mapValue"]["fields"]["individual_score"]["stringValue"] ===
        "19167299169928364486763899807280320784584689153446117019979075214178571216204"
    );
    setIndiviScore([{}]);
    setIndiviScore(filterScore);
    console.log(indivScore);
    console.log(
      "this",
      indivScore[0]["mapValue"]["fields"]["individual_score"]["stringValue"]
    );

    //console.log("Test", indivScore["mapValue"]);

    console.log("");
    */
    }

    let userID = 1235;
    let dbRef = db.collection("individual_scores");
    let query = dbRef
      .get()
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

          const findUserData = newdata.find((ui) => ui.user_id === userID);
          console.log(findUserData["individual_score"]);
          setIndiviScore(findUserData["individual_score"]);
        });
      })
      .catch((err) => {
        console.log("Error getting documents", err);
      });
  };

  return (
    <div>
      <h1>{indivScore}</h1>
      <h1>Firebase Data</h1>
      <h1>Firebase Data</h1>
    </div>
  );
};

export default FirebaseData;
