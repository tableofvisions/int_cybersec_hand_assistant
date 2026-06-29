import { NextAuthOptions, User } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: "Anmeldung",
      credentials: {
        username: { label: "E-Mail", type: "text" },
        password: { label: "Passwort", type: "password" },
      },
      async authorize(credentials): Promise<User | null> {
        try {
          // Step 1: Login → access_token
          const loginRes = await fetch(
            `${process.env.BACKEND_API_URL}/auth/login`,
            {
              method: "POST",
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              body: new URLSearchParams({
                username: credentials?.username ?? "",
                password: credentials?.password ?? "",
              }),
            }
          );
          if (!loginRes.ok) return null;
          const { access_token } = (await loginRes.json()) as {
            access_token: string;
          };

          // Step 2: /me → user details
          const meRes = await fetch(`${process.env.BACKEND_API_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${access_token}` },
          });
          if (!meRes.ok) return null;
          const me = (await meRes.json()) as {
            id: string;
            email: string;
            first_name: string;
            last_name: string;
            role: string;
            company_id: string;
          };

          return {
            accessToken: access_token,
            id: me.id,
            email: me.email,
            firstName: me.first_name,
            lastName: me.last_name,
            role: me.role,
            companyId: me.company_id,
          };
        } catch {
          return null;
        }
      },
    }),
  ],
  pages: { signIn: "/auth/login" },
  session: { strategy: "jwt" },
  callbacks: {
    // eslint-disable-next-line @typescript-eslint/require-await
    async jwt({ token, user, trigger }) {
      if (trigger === "signIn" && user) {
        return { ...token, ...user };
      }
      return token;
    },
    // eslint-disable-next-line @typescript-eslint/require-await
    async session({ session, token }) {
      session.user = {
        accessToken: token.accessToken as string,
        id: token.id as string,
        email: token.email as string,
        firstName: token.firstName as string,
        lastName: token.lastName as string,
        role: token.role as string,
        companyId: token.companyId as string,
      };
      return session;
    },
  },
} satisfies NextAuthOptions;
