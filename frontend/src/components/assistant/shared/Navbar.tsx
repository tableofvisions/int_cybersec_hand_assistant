import Image from "next/image";
import MobileNav from "@/components/assistant/shared/MobileNav";
import NavBarItems from "@/components/assistant/shared/NavBarItems";
import LoggedInUser from "@/components/assistant/shared/LoggedInUser";

const Navbar = () => {
  return (
    <>
      <div className="min-h-[50px] lg:min-h-[calc(100vh-200px)] bg-background drop-shadow-soft-1 mb-5 p-3">
        <div className="flex flex-between mt-3">
          <Image
            src="/assets/logos/ich-logo.webp"
            alt="Initiative Cybersicherheit Handwerk"
            priority
            width={180}
            height={53}
            className="max-sm:ms-3 sm:max-lg:ms-8"
          />
          <div className="flex items-center gap-2 lg:hidden">
            <LoggedInUser />
            <MobileNav />
          </div>
        </div>
        <nav className="lg:flex-between hidden my-10">
          <NavBarItems />
        </nav>
      </div>
    </>
  );
};

export default Navbar;
