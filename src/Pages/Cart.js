import React, { useState } from "react";

import { useCart } from "react-use-cart";
import emailjs from "emailjs-com";
let storeID0,storelink0,templateParams,storeID1,storeID2,storelink1,storelink2;

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
      storeID0 = link[0]["id"];
      storelink0 = link[0]["link"];
      templateParams = {
        subject,
        name,
        storeID0,
        storelink0,
      };
    }
    if (link.length === 2) {
      storeID0 = link[0]["id"];
      storelink0 = link[0]["link"];
      storeID1 = link[1]["id"];
      storelink1 = link[1]["link"];
      templateParams = {
        subject,
        name,
        storeID0,
        storelink0,
        storeID1,
        storelink1,
      };
    } else if (link.length > 2) {
      storeID0 = link[0]["id"];
      storelink0 = link[0]["link"];
      storeID1 = link[1]["id"];
      storelink1 = link[1]["link"];
      storeID2 = link[2]["id"];
      storelink2 = link[2]["link"];
      templateParams = {
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

    console.log(templateParams);

    emailjs
      .send(
        "service_hmvfb1i",
        "template_u5lvwyu",
        templateParams,
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

  const buyItems = () => {
    var t6 = performance.now();
    console.log("Item buy button clicked");
    const linksToOpen = []; // Array to store the links

    items.map((item, index) => {
   
      const linkUrl = `https://reputable-swagger-api.onrender.com/feedback/1235/${item.sellerID}/${random(
      params
    ).toFixed(0)}/1/`; 
      link.push({
        id: item.companyName,
        link: `https://reputable-swagger-api.onrender.com/feedback/1235/${item.sellerID}/${random(
          params
        ).toFixed(0)}/1/`,
      });
      linksToOpen.push(linkUrl); // Push the linkUrl into the array

    });
    console.log("feedback links", link);
    const t7 = performance.now();
    console.log(`Generate tokens time took ${t7 - t6} milliseconds.`);
    sendEmail();
    linksToOpen.forEach((linkUrl) => {
      window.open(linkUrl, "_blank");
    });
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
      <form action="https://reputable-swagger-api.onrender.com/" method="GET">
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