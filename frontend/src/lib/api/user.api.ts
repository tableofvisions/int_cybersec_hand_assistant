import "server-only";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/configs/auth";
import { handleError } from "../utils";
import type { BackendUser } from "@/types/assistant";

export type ApiUser = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  company_id: string;
  is_verified: boolean;
};

const ROLE_MAP: Record<string, BackendUser["roles"][number]> = {
  ADMIN: "OWNER",
  VIEWER: "USER",
};

function toBackendUser(u: ApiUser): BackendUser {
  return {
    id: u.id,
    firstName: u.first_name,
    lastName: u.last_name,
    mail: u.email,
    verified: u.is_verified,
    roles: [ROLE_MAP[u.role] ?? "USER"],
  };
}

export async function getUserData(): Promise<ApiUser | undefined> {
  try {
    const session = await getServerSession(authOptions);
    if (!session) return undefined;
    const res = await fetch(`${process.env.BACKEND_API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${session.user.accessToken}` },
      next: { revalidate: 3600 },
    });
    if (!res.ok) return undefined;
    return (await res.json()) as ApiUser;
  } catch (error) {
    handleError(error);
    return undefined;
  }
}

export async function getAllUsers(): Promise<BackendUser[] | undefined> {
  try {
    const session = await getServerSession(authOptions);
    if (!session) return undefined;
    const res = await fetch(`${process.env.BACKEND_API_URL}/users`, {
      headers: { Authorization: `Bearer ${session.user.accessToken}` },
      cache: "no-store",
    });
    if (!res.ok) return undefined;
    const data = (await res.json()) as ApiUser[];
    return data.map(toBackendUser);
  } catch (error) {
    handleError(error);
    return undefined;
  }
}
