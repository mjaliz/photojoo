import axios, { AxiosError } from "axios";
import { AppState } from "../context";

export interface Product {
  id: string;
  score: number;
  metadata: {
    name: string;
    current_price: number;
    category_name: string;
    image_url: string;
  };
}

interface Data {
  namespaces: string;
  matches: Product[];
}

export interface ApiResponse {
  namespaces: string;
  matches: Product[];
}

export interface ApiError {
  message: string;
  status: number | undefined;
}
export const fetchProducts = async (
  query: AppState
): Promise<ApiResponse | ApiError> => {
  try {
    let filtersQuery = "";
    if (query.price.priceLte > 0) {
      filtersQuery += `&price_gte=${query.price.priceGte}&price_lte=${query.price.priceLte}`;
    }
    const { data } = await axios.get<ApiResponse>(
      `http://localhost:8000/search/?query=${query.query}${filtersQuery}`
    );

    return data;
  } catch (error: unknown) {
    const err = error as AxiosError;
    return {
      message: err.message,
      status: err.response?.status,
    };
  }
};
