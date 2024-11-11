import { Product } from "../services/http";
import ProductItem from "./ProductItem";

interface ProductListProps {
  products: Product[];
}

export default function ProductList({ products }: ProductListProps) {
  console.log(products);

  return (
    <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-5">
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
