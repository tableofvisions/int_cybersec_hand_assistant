import "server-only";
import { EmergencyResourceContact, EmergencyResourcesData } from "@/types/assistant";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/configs/auth";
import { handleError } from "../utils";

export async function getEmergencyResourcesData(): Promise<
  EmergencyResourcesData | undefined
> {
  try {
    const session = await getServerSession(authOptions);
    if (!session) throw new Error("Not authenticated");

    const res = await fetch(
      `${process.env.BACKEND_API_URL}/incidents/emergency-contacts`,
      {
        headers: { Authorization: `Bearer ${session.user.accessToken}` },
        next: { revalidate: 60 * 60 },
      }
    );

    if (!res.ok) throw new Error("Emergency contacts could not be fetched");

    const contacts = (await res.json()) as EmergencyResourceContact[];
    return { contacts: contacts as [EmergencyResourceContact, ...EmergencyResourceContact[]] };
  } catch (error) {
    handleError(error);
    return undefined;
  }
}
