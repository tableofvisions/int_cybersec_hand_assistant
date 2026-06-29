"use server";
import "server-only";
import { revalidatePath } from "next/cache";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/configs/auth";
import { handleError } from "../utils";

type ProgressStatus = "OPEN" | "IN_PROGRESS" | "DONE" | "NOT_APPLICABLE";

async function authHeader(): Promise<Record<string, string>> {
  const session = await getServerSession(authOptions);
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (session) headers["Authorization"] = `Bearer ${session.user.accessToken}`;
  return headers;
}

export async function updateProgress(itemId: string, status: ProgressStatus): Promise<{ success: boolean; error?: string }> {
  try {
    const res = await fetch(`${process.env.BACKEND_API_URL}/progress/${itemId}`, {
      method: "PUT",
      headers: await authHeader(),
      body: JSON.stringify({ status }),
    });
    if (res.ok) {
      revalidatePath("/assistant/dashboard");
      revalidatePath("/assistant/measures");
      return { success: true };
    }
    const body = await res.json().catch(() => ({}));
    return { success: false, error: body?.detail ?? "Status konnte nicht gespeichert werden." };
  } catch (error) {
    handleError(error);
    return { success: false, error: "Netzwerkfehler. Bitte erneut versuchen." };
  }
}

export async function addComment(itemId: string, text: string): Promise<boolean> {
  try {
    const res = await fetch(`${process.env.BACKEND_API_URL}/progress/${itemId}/comments`, {
      method: "POST",
      headers: await authHeader(),
      body: JSON.stringify({ text }),
    });
    return res.ok;
  } catch (error) {
    handleError(error);
    return false;
  }
}
