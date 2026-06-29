import "next-auth";

declare module "next-auth" {
  interface User {
    accessToken: string;
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    role: string;
    companyId: string;
  }

  interface Session extends DefaultSession {
    user: User;
    expires: string;
  }
}
