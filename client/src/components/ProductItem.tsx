import { Card, CardBody, CardFooter, Image } from "@nextui-org/react";

interface ProductItemProps {
  name: string;
  imgUrl: string;
  price: number;
  category: string;
}

export default function ProductItem({
  name,
  imgUrl,
  price,
  category,
}: ProductItemProps) {
  return (
    <Card className="py-4">
      <CardBody className="overflow-visible py-2 items-center">
        <Image
          alt="Card background"
          className="object-cover rounded-xl"
          src={imgUrl}
          width={300}
          height={300}
        />
      </CardBody>
      <CardFooter className="flex flex-col items-start">
        <p>Category: {category !== "" ? category : "Other"}</p>
        <p>Name: {name}</p>
        <p>Price: {price}</p>
      </CardFooter>
    </Card>
  );
}
