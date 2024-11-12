import { FormEvent, useContext, useState } from "react";
import { Navbar, NavbarContent, Input } from "@nextui-org/react";
import { SearchIcon } from "../icons/SearchIcon";

import AppContext from "../context";

export default function AppNavbar() {
  const { setQuery } = useContext(AppContext);
  const [input, setInput] = useState("");
  const handleFormSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input !== "") {
      setQuery(input);
    }
  };
  return (
    <Navbar isBordered>
      <NavbarContent className="items-center w-full" justify="center">
        <form onSubmit={handleFormSubmit} className="w-full">
          <Input
            classNames={{
              base: "w-full h-10",
              mainWrapper: "h-full",
              input: "text-small",
              inputWrapper:
                "h-full font-normal text-default-500 bg-default-400/20 dark:bg-default-500/20",
            }}
            placeholder="What dress you looking for..."
            size="md"
            startContent={<SearchIcon size={18} />}
            type="search"
            value={input}
            onValueChange={setInput}
          />
        </form>
      </NavbarContent>
    </Navbar>
  );
}
