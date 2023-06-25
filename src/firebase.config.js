//import firebase from 'firebase';
import { initializeApp } from "firebase/app";
import { getFirestore } from  "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDD0ntPx8CiICDYUHuXCod1HjRmQGUDUmk",
  authDomain: "reputable-b7df1.firebaseapp.com",
  projectId: "reputable-b7df1",
  storageBucket: "reputable-b7df1.appspot.com",
  messagingSenderId: "802223406358",
  appId: "1:802223406358:web:cad6c3f608b1165a67a437",
};

const firebaseApp = initializeApp(firebaseConfig);

//const database=firebase.firestore();
const database = getFirestore(firebaseApp);


export default database;