import React from "react";
import { useCart } from "react-use-cart";

const Itemcard = (props) => {
  const { addItem } = useCart();

  function testClick() {
    console.log("this happended");
  }

  return (
    <div className="col-11 col-md-6 col-lg-3">
      <div class="card p-0 overflow-hidden h-100 shadow">
        <img src={props.img} class="card-img-top img-fluid" alt="" />
        <div class="card-body text-center">
          <h5 class="card-title">{props.title}</h5>
          <h5 class="card-title">£{props.price}</h5>
          <p class="card-text"> {props.desc}</p>
          <h5 class="card-title">Seller: {props.companyName}</h5>
          <button class="btn btn-success" onClick={() => addItem(props.item)}>
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
};

export default Itemcard;
