import { Card, CardBody, CardFooter, Image } from "@nextui-org/react";

interface ProductItemProps {
  name: string;
  imgUrl: string;
}

export default function ProductItem({ name, imgUrl }: ProductItemProps) {
  console.log(imgUrl);

  return (
    <Card className="py-4">
      <CardBody className="overflow-visible py-2 w-full">
        <Image
          alt="Card background"
          className="object-cover rounded-xl w-full"
          src={imgUrl}
        />
      </CardBody>
      <CardFooter>
        <p>{name}</p>
      </CardFooter>
    </Card>
  );
}
