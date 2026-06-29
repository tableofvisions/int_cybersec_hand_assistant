import { getAreas } from "@/lib/api/checklist.api";
import Header from "@/components/assistant/shared/Header";
import Link from "next/link";
import { Suspense } from "react";
import AreaRadarChart from "@/components/assistant/widgets/AreaRadarChart";
import BsiFeedSection from "@/components/assistant/widgets/BsiFeedSection";
import CollapsibleSection from "@/components/assistant/shared/CollapsibleSection";

const AREA_ICONS: Record<string, string> = {
  "mensch-organisation": "groups",
  "technik-systeme":     "computer",
  "sicherheit-zugang":   "lock",
  "risiko-notfall":      "warning",
};

export default async function DashboardPage() {
  const areas = await getAreas();

  return (
    <>
      <Header title="IT-Sicherheitsassistent" />

      {areas.length === 0 ? (
        <div className="mt-8 rounded-xl border border-dashed border-gray-300 p-10 text-center text-gray-500">
          <p className="text-lg font-medium">Keine Daten vorhanden</p>
          <p className="mt-1">Die LLM-Mapping-Pipeline muss zuerst ausgeführt werden.</p>
        </div>
      ) : (
        <CollapsibleSection
          title="Fortschritt nach Bereich"
          storageKey="dashboard-section-progress"
          defaultOpen={true}
        >
          {/* 2×2 area cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {areas.map((area) => {
              const done       = area.done;
              const inProgress = area.in_progress;
              const notAppl    = area.not_applicable;
              const open       = area.total_items - done - inProgress - notAppl;
              const pct        = area.total_items > 0
                ? Math.round((done / area.total_items) * 100)
                : 0;

              return (
                <Link
                  key={area.slug}
                  href={`/assistant/measures?area=${area.slug}`}
                  className="block rounded-xl border border-gray-200 bg-white p-5 shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start gap-3 mb-4">
                    <div className="shrink-0 w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center">
                      <i className="material-symbols-outlined text-gray-500">
                        {AREA_ICONS[area.slug] ?? "category"}
                      </i>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 leading-tight">{area.name}</h4>
                      <p className="text-gray-400">{area.total_items} Maßnahmen</p>
                    </div>
                  </div>

                  <div className="flex h-1.5 rounded-full overflow-hidden bg-gray-100 mb-3">
                    {done > 0 && (
                      <div className="bg-green-500" style={{ width: `${(done / area.total_items) * 100}%` }} />
                    )}
                    {inProgress > 0 && (
                      <div className="bg-yellow-400" style={{ width: `${(inProgress / area.total_items) * 100}%` }} />
                    )}
                    {notAppl > 0 && (
                      <div className="bg-gray-300" style={{ width: `${(notAppl / area.total_items) * 100}%` }} />
                    )}
                  </div>

                  <div className="flex justify-between text-gray-500">
                    <span className="font-medium text-green-600">{pct} % abgeschlossen</span>
                    <span>{open} offen · {inProgress} in Bearbeitung</span>
                  </div>
                </Link>
              );
            })}
          </div>

          {/* Spider chart + legend */}
          <div className="mt-4 rounded-xl border border-gray-200 bg-white px-6 shadow-sm">
            <div className="flex flex-col sm:flex-row items-center gap-6 my-5">
              <div className="shrink-0 w-full sm:w-80 my-6">
                <AreaRadarChart areas={areas} />
              </div>
              <div className="flex-1 min-w-0 w-full space-y-4">
                {areas.map((area) => {
                  const pct         = area.total_items > 0 ? Math.round((area.done / area.total_items) * 100) : 0;
                  const doneW       = area.total_items > 0 ? (area.done / area.total_items) * 100 : 0;
                  const inProgressW = area.total_items > 0 ? (area.in_progress / area.total_items) * 100 : 0;
                  const naW         = area.total_items > 0 ? (area.not_applicable / area.total_items) * 100 : 0;
                  return (
                    <div key={area.slug}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="flex items-center gap-2 font-medium text-gray-700">
                          <i className="material-symbols-outlined text-gray-400">
                            {AREA_ICONS[area.slug] ?? "category"}
                          </i>
                          {area.name}
                        </span>
                        <span className="font-semibold text-green-600">{pct} %</span>
                      </div>
                      <div className="flex h-2 rounded-full overflow-hidden bg-gray-100">
                        {doneW > 0 && <div className="bg-green-500" style={{ width: `${doneW}%` }} />}
                        {inProgressW > 0 && <div className="bg-yellow-400" style={{ width: `${inProgressW}%` }} />}
                        {naW > 0 && <div className="bg-gray-300" style={{ width: `${naW}%` }} />}
                      </div>
                    </div>
                  );
                })}
                <div className="flex flex-wrap gap-4 pt-1 text-gray-500">
                  <span className="flex items-center gap-1.5"><span className="inline-block w-3 h-3 rounded-full bg-green-500" />Erledigt</span>
                  <span className="flex items-center gap-1.5"><span className="inline-block w-3 h-3 rounded-full bg-yellow-400" />In Bearbeitung</span>
                  <span className="flex items-center gap-1.5"><span className="inline-block w-3 h-3 rounded-full bg-gray-300" />Nicht zutreffend</span>
                </div>
              </div>
            </div>
          </div>
        </CollapsibleSection>
      )}

      <CollapsibleSection
        title="Aktuelle IT-Sicherheitswarnungen"
        storageKey="dashboard-section-bsi-feed"
        defaultOpen={true}
      >
        <Suspense fallback={
          <div className="rounded-xl border border-gray-200 bg-white p-6 text-gray-400 animate-pulse">
            Lade IT-Sicherheitswarnungen…
          </div>
        }>
          <BsiFeedSection />
        </Suspense>
      </CollapsibleSection>
    </>
  );
}
