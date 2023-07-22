import { Button } from "bootstrap";
import React, { useState } from "react";

import { useCart } from "react-use-cart";
import emailjs from "emailjs-com";

//import Alert from "react-bootstrap/Alert";

const Cart = () => {
  const {
    isEmpty,
    totalUniqueItems,
    items,
    cartTotal,
    updateItemQuantity,
    removeItem,
    emptyCart,
  } = useCart();
  const [show, setShow] = useState(false);
  const subject = "The Fruit Shop Feedback";
  const name = "User";
  const link = [];

  const sendEmail = () => {
    if (link.length === 1) {
      console.log("I am in send email");
      var storeID0 = link[0]["id"];
      var storelink0 = link[0]["link"];
      var templatePrams = {
        subject,
        name,
        storeID0,
        storelink0,
      };
    }
    if (link.length === 2) {
      var storeID0 = link[0]["id"];
      var storelink0 = link[0]["link"];
      var storeID1 = link[1]["id"];
      var storelink1 = link[1]["link"];
      var templatePrams = {
        subject,
        name,
        storeID0,
        storelink0,
        storeID1,
        storelink1,
      };
    } else if (link.length > 2) {
      var storeID0 = link[0]["id"];
      var storelink0 = link[0]["link"];
      var storeID1 = link[1]["id"];
      var storelink1 = link[1]["link"];
      var storeID2 = link[2]["id"];
      var storelink2 = link[2]["link"];
      var templatePrams = {
        subject,
        name,
        storeID0,
        storelink0,
        storeID1,
        storelink1,
        storeID2,
        storelink2,
      };
    }

    console.log(templatePrams);

    emailjs
      .send(
        "service_hmvfb1i",
        "template_u5lvwyu",
        templatePrams,
        "user_JpXI2W5UX9jJ1RG0X0J5H"
      )
      .then(
        function (response) {
          console.log("SUCCESS! email sent!", response.status, response.text);
        },
        function (error) {
          console.log("FAILED...", error);
        }
      );
  };
  //const feedbackList = [];

  const buyItems = () => {
    var t6 = performance.now();
    console.log("Item buy button clicked");
    items.map((item, index) => {
      // console.log("Unique seller name: " + item.companyName);
      // console.log(
      //   `http://localhost:3000/feedback/4345/${item.sellerID}/${random(
      //     params
      //   ).toFixed(0)}/1/`
      // );
      
      link.push({
        id: item.companyName,
        link: `https://reputable.onrender.com/feedback/1235/${item.sellerID}/${random(
          params
        ).toFixed(0)}/1/`,
      });
    });
    console.log("feedback link", link);
    const t7 = performance.now();
    console.log(`Generate tokens time took ${t7 - t6} milliseconds.`);
    sendEmail();
    setShow(true);
  };

  const random = require("simple-random-number-generator");
  let params = {
    min: 4000000,
    max: 5000000,
  };
  const emptyCartandShowAlert = () => {
    setShow(false);
    emptyCart();
  };
  if (isEmpty)
    return (
      <h1 className="text-Center row justify-content-center">
        Your Cart is Empty
      </h1>
    );
  if (show)
    return (
      <div
        class="text-Center row justify-content-center alert alert-warning alert-dismissible fade show"
        role="alert"
      >
        <h2 className="text-Center row justify-content-center">
          Successful! Your order is confirmed.
        </h2>

        {/* {items.map((item, index) => {
            // idandlinks.push({ id: item.sellerID, link: "asdadsd" });
            items.forEach((item) => {
              console.log("asda" + item.sellerID);
            });

            // return (

            //   <a>
            //     <Link
            //       // target="_blank"
            //       className="text-Center row justify-content-center fs-6 font-weight-light"
            //       to={{
            //         pathname: `feedback/4345/${item.sellerID}/${random(
            //           params
            //         ).toFixed(0)}/1/`,
            //         state: { fromDashboard: item.companyName },
            //       }}
            //       target="_blank"
            //     >
            //       <h4 className="text-Center row justify-content-center">
            //         {item.companyName} : {item.title}
            //       </h4>
            //     </Link>
            //   </a>
            // );
          })}*/}

        <h8 className="text-Center row justify-content-center">
          {" "}
          Check email for further updates!
        </h8>

        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
          onClick={() => emptyCartandShowAlert()}
        ></button>
      </div>
    );

  return (
    <section className="py-4 container">
      <form action="https://reputable.onrender.com/" method="GET">
        <div className="row justify-content-center">
          <div className="col-12"></div>
          <h5>Your Cart has {totalUniqueItems} Items</h5>
          <table className="table table-light table-hover m-0">
            <tbody>
              {items.map((item, index) => {
                return (
                  <tr key={index}>
                    <td>
                      <img src={item.img} style={{ height: "6rem" }} alt="" />
                    </td>
                    <td>{item.title}</td>
                    <td>£{item.price}</td>
                    <td>Quantity: ({item.quantity}) </td>

                    <td>
                      <button
                        className="btn btn-info ms-2"
                        onClick={() =>
                          updateItemQuantity(item.id, item.quantity - 1)
                        }
                      >
                        -
                      </button>
                      <button
                        className="btn btn-info ms-2"
                        onClick={() =>
                          updateItemQuantity(item.id, item.quantity + 1)
                        }
                      >
                        +
                      </button>
                      <button
                        className="btn btn-danger ms-2"
                        onClick={() => removeItem(item.id)}
                      >
                        Remove Item
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="col-auto ms-auto flexBox">
          <h2>Total: £{cartTotal.toFixed(2)}</h2>
        </div>
        <div className="col-auto">
          <button className="btn btn-danger m-2" onClick={() => emptyCart()}>
            Remove All Items
          </button>
          <button className="btn btn-success m-2" onClick={() => buyItems()}>
            Buy Now
          </button>
        </div>
      </form>
    </section>
  );
};
export default Cart;