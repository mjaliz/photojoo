import { Button, Slider } from "@nextui-org/react";
import { FormEvent, useContext, useState } from "react";
import AppContext from "../context";

export default function Filters() {
  const { appState, setPrice } = useContext(AppContext);
  const [pricesFilter, setPricesFilter] = useState([
    appState.price.priceGte,
    appState.price.priceLte,
  ]);
  const handleFormSubmit = (e: FormEvent) => {
    e.preventDefault();
    setPrice({ priceGte: pricesFilter[0], priceLte: pricesFilter[1] });
  };
  const handleChange = (value: number | number[]) => {
    const prices = value as number[];
    setPricesFilter(prices);
  };
  return (
    <div className="flex flex-col">
      <form onSubmit={handleFormSubmit}>
        <Slider
          label="Price Range"
          step={10}
          minValue={0}
          maxValue={1000}
          defaultValue={pricesFilter}
          formatOptions={{ style: "currency", currency: "USD" }}
          className=""
          onChange={handleChange}
        />
        <Button
          type="submit"
          variant="solid"
          color="primary"
          fullWidth
          className="mt-8"
        >
          Save
        </Button>
      </form>
    </div>
  );
}
