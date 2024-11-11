import { useContext, useEffect, useState } from "react";
import AppNavbar from "./components/AppNavbar";
import AppContext from "./context";
import { ApiResponse, fetchProducts, Product } from "./services/http";
import ProductList from "./components/ProductList";
import AppSkeleton from "./components/AppSkeleton";
import Filters from "./components/Filters";

function App() {
  const { appState, setProducts } = useContext(AppContext);
  useEffect(() => {
    const fetchItems = async () => {
      const res = await fetchProducts(appState);
      const resp = res as ApiResponse;

      if (resp.matches !== undefined) {
        setProducts(resp.matches);
      }
    };
    if (appState.query !== "") {
      fetchItems();
    }
  }, [appState.query, appState.price, appState.categoryName]);

  return (
    <>
      <AppNavbar />
      <div className="container mx-auto grid grid-cols-7 2xl:grid-cols-6 gap-10 py-5">
        <div className="col-span-5">
          <ProductList products={appState.products} />
        </div>
        <div className="col-span-2 2xl:col-span-1">
          <Filters />
        </div>
      </div>
    </>
  );
}

export default App;
