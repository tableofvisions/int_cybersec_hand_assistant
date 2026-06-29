"use client";

import SpiderDiagram from "@/components/assistant/shared/SpiderDiagram";
import { Area } from "@/lib/api/checklist.api";

const SHORT_LABELS: Record<string, string> = {
  "mensch-organisation": "Mensch &\nOrganisation",
  "technik-systeme":     "Technik &\nSysteme",
  "sicherheit-zugang":   "Sicherheit &\nZugang",
  "risiko-notfall":      "Risiko &\nNotfall",
};

export default function AreaRadarChart({ areas }: { areas: Area[] }) {
  const data = areas.map((area) => {
    const pct = area.total_items > 0 ? area.done / area.total_items : 0;
    return {
      label: SHORT_LABELS[area.slug] ?? area.name,
      display: pct,
      value: pct,
    };
  });

  const allZero = data.every((d) => d.value === 0);

  if (allZero) {
    return (
      <p className="text-gray-400 text-center py-8">
        Noch kein Fortschritt erfasst
      </p>
    );
  }

  const maxPct = Math.max(...data.map((d) => d.value));
  const upperBound = maxPct <= 0.25 ? 0.25 : maxPct <= 0.5 ? 0.5 : maxPct <= 0.75 ? 0.75 : 1;
  const normalized = data.map((d) => ({ ...d, display: d.value / upperBound }));
  return (
    <div className="w-full px-10 py-6 -ml-2">
      <SpiderDiagram data={normalized} width={220} height={200} radiusScale={0.36} />
    </div>
  );
}
