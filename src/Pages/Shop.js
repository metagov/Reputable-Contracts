import React from "react";
import Itemcard from "../Resources/Itemcard";
import data from "../Resources/data";

const Shop = () => {
  console.warn(data.fruitData);
  return (
    <div>
      <h1 className="text-center mt-3">Featured Items</h1>
      <section className="py-4 container">
        <div className="row justify-content-center">
          {data.fruitData.map((item, index) => {
            return (
              <Itemcard
                img={item.img}
                title={item.title}
                desc={item.desc}
                price={item.price}
                companyName={item.companyName}
                item={item}
                key={index}
              />
            );
          })}
        </div>
      </section>
    </div>
  );
};

export default Shop;
