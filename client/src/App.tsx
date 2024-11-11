import { useContext, useEffect } from "react";
import AppNavbar from "./components/AppNavbar";
import AppContext from "./context";
import { fetchProducts } from "./services/http";

function App() {
  const { appState } = useContext(AppContext);
  useEffect(() => {
    const fetchItems = async () => {
      const res = await fetchProducts(appState);
      console.log(res);
    };
    if (appState.query !== "") {
      fetchItems();
    }
  }, [appState]);

  return (
    <>
      <AppNavbar />
    </>
  );
}

export default App;
