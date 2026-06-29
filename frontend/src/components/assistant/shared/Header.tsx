import LoggedInUser from "@/components/assistant/shared/LoggedInUser";

const Header = ({ title }: { title: string }) => {
  return (
    <div className="flex flex-row items-center justify-between mb-8 mt-4">
      <h1 className="font-bold hyphens-auto">{title}</h1>
      <div className="hidden lg:block">
        <LoggedInUser />
      </div>
    </div>
  );
};

export default Header;
