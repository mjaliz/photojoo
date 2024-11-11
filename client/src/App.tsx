import { useContext, useEffect, useState } from "react";
import AppNavbar from "./components/AppNavbar";
import AppContext from "./context";
import { ApiResponse, fetchProducts, Product } from "./services/http";
import ProductList from "./components/ProductList";

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
  }, [appState.query]);

  return (
    <>
      <AppNavbar />
      <div className="container mx-auto">
        <ProductList products={appState.products} />
      </div>
    </>
  );
}

export default App;
