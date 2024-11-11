import React from "react";
import { Product } from "../services/http";
import ProductItem from "./ProductItem";

interface ProductListProps {
  products: Product[];
}

export default function ProductList({ products }: ProductListProps) {
  console.log(products);

  return (
    <div className="grid grid-cols-3 xl:grid-cols-5 2xl:grid-cols-6 gap-5 mt-5">
      {products.map((p, _) => (
        <ProductItem
          key={p.id}
          name={p.metadata.name}
          imgUrl={p.metadata.image_url}
          price={p.metadata.current_price}
          category={p.metadata.category_name}
        />
      ))}
    </div>
  );
}
