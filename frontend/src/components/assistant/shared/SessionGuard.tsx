"use client";

import { useSession, signOut } from "next-auth/react";
import { useEffect } from "react";

export default function SessionGuard() {
  const { data: session } = useSession();

  useEffect(() => {
    const token = session?.user?.accessToken;
    if (!token) return;

    let exp: number;
    try {
      const payload = JSON.parse(atob(token.split(".")[1])) as { exp: number };
      exp = payload.exp * 1000;
    } catch {
      return;
    }

    const delay = exp - Date.now();

    const logout = () =>
      void signOut({ redirect: false }).then(() => {
        window.location.href = "/auth/login";
      });

    if (delay <= 0) {
      logout();
      return;
    }

    const timer = setTimeout(logout, delay);
    return () => clearTimeout(timer);
  }, [session?.user?.accessToken]);

  return null;
}
