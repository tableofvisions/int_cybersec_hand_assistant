import Link from "next/link";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/configs/auth";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuGroup,
} from "@/components/ui/dropdown-menu";
import SignOut from "./SignOut";

const ROLE_LABELS: Record<string, string> = {
  ADMIN: "Administrator",
  EDITOR: "Bearbeiter",
  VIEWER: "Betrachter",
};

const LoggedInUser = async () => {
  const session = await getServerSession(authOptions);
  if (!session) return null;

  const { firstName, lastName, role } = session.user;
  const initials = `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();

  return (
    <div className="flex flex-row gap-2 items-center">
      <DropdownMenu>
        <DropdownMenuTrigger className="group flex items-center gap-2 outline-none">
          <Avatar>
            <AvatarFallback className="bg-highlight-50 text-white text-lg font-bold">
              {initials}
            </AvatarFallback>
          </Avatar>
          <div className="hidden sm:flex flex-col text-left">
            <p className="font-bold">{firstName} {lastName}</p>
            <p className="text-sm text-gray-500">{ROLE_LABELS[role] ?? role}</p>
          </div>
          <span className="hidden lg:block">
            <i className="material-symbols-outlined md-l transition-transform duration-200 group-data-[state=open]:rotate-180">
              expand_more
            </i>
          </span>
        </DropdownMenuTrigger>
        <DropdownMenuContent collisionPadding={40} className="p-2">
          <DropdownMenuLabel className="text-base flex flex-row gap-2 pe-8">
            <i className="material-symbols-outlined md-xl filled">person</i>
            <div>
              <div>Benutzerkonto</div>
              <div className="text-sm font-normal">{ROLE_LABELS[role] ?? role}</div>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem className="flex flex-row gap-3 text-base hover:bg-highlight-50 hover:text-tc-contrast px-4">
              <i className="material-symbols-outlined md-m">tune</i>
              <Link href="/assistant/settings">Einstellungen</Link>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem className="flex flex-row gap-3 text-base hover:bg-highlight-50 hover:text-tc-contrast px-4">
              <i className="material-symbols-outlined md-m">logout</i>
              <SignOut />
            </DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

export default LoggedInUser;
