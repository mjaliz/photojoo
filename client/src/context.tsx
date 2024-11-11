import { createContext, useState } from "react";
import { PropsWithChildren } from "react";

interface AppContextType {
  appState: AppState;
  setQuery: (query: string) => void;
  setCategoryName: (categoryName: string) => void;
  setPrice: (price: PriceFilter) => void;
}
export interface AppState {
  query: string;
  categoryName: string;
  price: PriceFilter;
}
export interface PriceFilter {
  priceGte: number;
  priceLte: number;
}

const initialState: AppState = {
  query: "",
  categoryName: "",
  price: { priceGte: 0, priceLte: 10000000 },
};

const defaultContext: AppContextType = {
  appState: {
    query: "",
    categoryName: "",
    price: { priceGte: 0, priceLte: 10000000 },
  },
  setQuery: () => {},
  setCategoryName: () => {},
  setPrice: () => {},
};

const AppContext = createContext<AppContextType>(defaultContext);

export function AppProvider({ children }: PropsWithChildren) {
  const [appState, setAppState] = useState<AppState>(initialState);

  const setQuery = (query: string) => {
    setAppState({ ...appState, query });
  };
  const setCategoryName = (categoryName: string) => {
    setAppState({ ...appState, categoryName });
  };
  const setPrice = (price: PriceFilter) => {
    setAppState({ ...appState, price });
  };

  return (
    <AppContext.Provider
      value={{ appState, setQuery, setPrice, setCategoryName }}
    >
      {children}
    </AppContext.Provider>
  );
}
export default AppContext;
