"use client";

import { signOut } from "next-auth/react";
import Link from "next/link";

const SignOut = () => {
  return (
    <Link
      href="#"
      onClick={async (e) => {
        e.preventDefault();
        await signOut({ redirect: false });
        window.location.href = "/auth/login";
      }}
    >
      Abmelden
    </Link>
  );
};

export default SignOut;
