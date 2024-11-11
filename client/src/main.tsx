import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { NextUIProvider } from "@nextui-org/react";

import "./index.css";
import App from "./App.tsx";
import { AppProvider } from "./context.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <NextUIProvider>
      <AppProvider>
        <App />
      </AppProvider>
    </NextUIProvider>
  </StrictMode>
);
