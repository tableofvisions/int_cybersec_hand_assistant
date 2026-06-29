import "server-only";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/configs/auth";
import { handleError } from "../utils";

export type IncidentSign = {
  id: string;
  title: string;
  description: string;
  examples: string[];
};

export type IncidentStep = {
  pos: number;
  title: string;
  text: string;
  sourceLabel?: string;
  sourceUrl?: string;
};

export type IncidentLink = {
  title: string;
  url: string;
};

export type IncidentLinkCategory = {
  id: string;
  title: string;
  links: IncidentLink[];
};

async function authHeader(): Promise<Record<string, string>> {
  const session = await getServerSession(authOptions);
  if (session) return { Authorization: `Bearer ${session.user.accessToken}` };
  return {};
}

export async function getIncidentSigns(): Promise<IncidentSign[]> {
  try {
    const res = await fetch(`${process.env.BACKEND_API_URL}/incidents/signs`, {
      headers: await authHeader(),
      next: { revalidate: 60 * 60 * 24 },
    });
    if (!res.ok) return [];
    return (await res.json()) as IncidentSign[];
  } catch (error) {
    handleError(error);
    return [];
  }
}

export async function getIncidentSteps(): Promise<IncidentStep[]> {
  try {
    const res = await fetch(`${process.env.BACKEND_API_URL}/incidents/steps`, {
      headers: await authHeader(),
      next: { revalidate: 60 * 60 * 24 * 7 },
    });
    if (!res.ok) return [];
    return (await res.json()) as IncidentStep[];
  } catch (error) {
    handleError(error);
    return [];
  }
}

export async function getIncidentLinks(): Promise<IncidentLinkCategory[]> {
  try {
    const res = await fetch(`${process.env.BACKEND_API_URL}/incidents/links`, {
      headers: await authHeader(),
      next: { revalidate: 60 * 60 * 24 },
    });
    if (!res.ok) return [];
    return (await res.json()) as IncidentLinkCategory[];
  } catch (error) {
    handleError(error);
    return [];
  }
}
