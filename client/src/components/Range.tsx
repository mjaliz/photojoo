import { Slider } from "@nextui-org/react";
import { useContext } from "react";
import AppContext from "../context";

export default function Range() {
  const { appState, setPrice } = useContext(AppContext);
  const handleChange = (value: number | number[]) => {
    const prices = value as number[];
    console.log(prices);

    setPrice({ priceGte: prices[0], priceLte: prices[1] });
  };
  return (
    <Slider
      label="Price Range"
      step={10}
      minValue={0}
      maxValue={1000}
      defaultValue={[appState.price.priceGte, appState.price.priceLte]}
      formatOptions={{ style: "currency", currency: "USD" }}
      className=""
      onChange={handleChange}
    />
  );
}
