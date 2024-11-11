import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Input,
  DropdownItem,
  DropdownTrigger,
  Dropdown,
  DropdownMenu,
  Avatar,
} from "@nextui-org/react";
import { SearchIcon } from "../icons/SearchIcon";

export default function AppNavbar() {
  return (
    <Navbar isBordered>
      <NavbarContent className="items-center w-full" justify="center">
        <Input
          classNames={{
            base: "w-full h-10",
            mainWrapper: "h-full",
            input: "text-small",
            inputWrapper:
              "h-full font-normal text-default-500 bg-default-400/20 dark:bg-default-500/20",
          }}
          placeholder="Type to search..."
          size="md"
          startContent={<SearchIcon size={18} />}
          type="search"
        />
      </NavbarContent>
    </Navbar>
  );
}
