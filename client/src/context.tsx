import { createContext, useState } from "react";
import { PropsWithChildren } from "react";
import { Product } from "./services/http";

interface AppContextType {
  appState: AppState;
  setQuery: (query: string) => void;
  setCategoryName: (categoryName: string) => void;
  setPrice: (price: PriceFilter) => void;
  setProducts: (products: Product[]) => void;
}
export interface AppState {
  products: Product[];
  query: string;
  categoryName: string;
  price: PriceFilter;
}
export interface PriceFilter {
  priceGte: number;
  priceLte: number;
}

const initialState: AppState = {
  products: [],
  query: "",
  categoryName: "",
  price: { priceGte: 0, priceLte: 10000000 },
};

const defaultContext: AppContextType = {
  appState: {
    products: [],
    query: "",
    categoryName: "",
    price: { priceGte: 0, priceLte: 10000000 },
  },
  setQuery: () => {},
  setCategoryName: () => {},
  setPrice: () => {},
  setProducts: () => {},
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

  const setProducts = (products: Product[]) => {
    console.log(products);

    setAppState({ ...appState, products });
  };

  return (
    <AppContext.Provider
      value={{ appState, setQuery, setPrice, setCategoryName, setProducts }}
    >
      {children}
    </AppContext.Provider>
  );
}
export default AppContext;
