import { useContext } from "react";
import AppNavbar from "./components/AppNavbar";
import AppContext from "./context";

function App() {
  const { appState } = useContext(AppContext);
  console.log(appState.query, "querrrryyyyyyyy from navbars");

  return (
    <>
      <AppNavbar />
    </>
  );
}

export default App;
