"use client";

import { NotificationsProvider } from "@/contexts/NotificationsProvider";
import { SessionProvider } from "next-auth/react";

function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider refetchOnWindowFocus={false}>
      <NotificationsProvider>{children}</NotificationsProvider>
    </SessionProvider>
  );
}

export default Providers;
