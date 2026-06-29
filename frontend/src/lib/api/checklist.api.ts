import "server-only";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/configs/auth";
import { handleError } from "../utils";

export type Area = {
  id: string;
  slug: string;
  name: string;
  emoji: string | null;
  sort_order: number;
  total_items: number;
  done: number;
  in_progress: number;
  not_applicable: number;
};

export type MeasureRef = {
  control_id: string;
  parent_control_id: string | null;
  group_id: string;
  group_title: string;
  subgroup_id: string;
  subgroup_title: string;
  title: string;
  requirement_text: string;
  guidance_text: string | null;
  sec_level: string;
  effort_level: number;
};

export type ChecklistItem = {
  id: string;
  short_description: string | null;
  confidence: number;
  priority: number | null;
  area_slug: string;
  area_name: string;
  measure: MeasureRef;
  status: "OPEN" | "IN_PROGRESS" | "DONE" | "NOT_APPLICABLE";
  progress_id: string | null;
  updated_at: string | null;
  comment_count: number;
};

async function authHeader(): Promise<Record<string, string>> {
  const session = await getServerSession(authOptions);
  if (session) return { Authorization: `Bearer ${session.user.accessToken}` };
  return {};
}

export async function getAreas(): Promise<Area[]> {
  try {
    const res = await fetch(`${process.env.BACKEND_API_URL}/areas`, {
      headers: await authHeader(),
      cache: "no-store",
    });
    if (!res.ok) return [];
    return (await res.json()) as Area[];
  } catch (error) {
    handleError(error);
    return [];
  }
}

export async function getChecklistItems(areaSlug?: string, status?: string): Promise<ChecklistItem[]> {
  try {
    const params = new URLSearchParams();
    if (areaSlug) params.set("area_slug", areaSlug);
    if (status) params.set("status", status);
    const url = `${process.env.BACKEND_API_URL}/checklist${params.size ? `?${params}` : ""}`;
    const res = await fetch(url, {
      headers: await authHeader(),
      cache: "no-store",
    });
    if (!res.ok) return [];
    return (await res.json()) as ChecklistItem[];
  } catch (error) {
    handleError(error);
    return [];
  }
}

export async function getChecklistItem(id: string): Promise<ChecklistItem | undefined> {
  try {
    const res = await fetch(`${process.env.BACKEND_API_URL}/checklist/${id}`, {
      headers: await authHeader(),
      cache: "no-store",
    });
    if (!res.ok) return undefined;
    return (await res.json()) as ChecklistItem;
  } catch (error) {
    handleError(error);
    return undefined;
  }
}
