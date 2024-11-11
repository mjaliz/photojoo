import { Slider } from "@nextui-org/react";

export default function Range() {
  return (
    <Slider
      label="Price Range"
      step={5}
      minValue={0}
      maxValue={1000}
      defaultValue={[100, 500]}
      formatOptions={{ style: "currency", currency: "USD" }}
      className=""
    />
  );
}
