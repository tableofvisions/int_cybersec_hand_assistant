"use client";

import Image from "next/image";
import { Separator } from "@/components/ui/separator";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import React, { useState } from "react";
import NavBarItems from "./NavBarItems";

const MobileNav = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  return (
    <nav className="lg:hidden">
      <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
        <SheetTrigger className="align-middle me-3">
          <i className="material-symbols-outlined md-l">menu</i>
        </SheetTrigger>
        <SheetContent className="flex flex-col gap-6 bg-background max-[350px]:w-full">
          <SheetHeader>
            <SheetTitle></SheetTitle>
          </SheetHeader>
          <SheetDescription></SheetDescription>
          <Image
            src="/assets/logos/ich-logo.webp"
            alt="Initiative Cybersicherheit Handwerk"
            width={180}
            height={53}
          />
          <NavBarItems setMenuOpen={setMenuOpen} />
          <Separator className="border border-contrast-verylight" />
        </SheetContent>
      </Sheet>
    </nav>
  );
};

export default MobileNav;
