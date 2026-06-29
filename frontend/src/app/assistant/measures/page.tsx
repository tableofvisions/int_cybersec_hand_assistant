import { getAreas, getChecklistItems } from "@/lib/api/checklist.api";
import Header from "@/components/assistant/shared/Header";
import ChecklistTable from "@/components/assistant/checklist/ChecklistTable";
import Link from "next/link";

type SearchParams = { area?: string; status?: string };

export default async function MeasuresPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>;
}) {
  const { area, status } = await searchParams;
  const [areas, items] = await Promise.all([
    getAreas(),
    getChecklistItems(area, status),
  ]);

  const activeArea = areas.find((a) => a.slug === area);

  return (
    <>
      <Header title={activeArea ? activeArea.name : "ITSM-Maßnahmen"} />

      {/* Area filter tabs */}
      <div className="flex flex-wrap gap-2 mt-4 mb-6">
        <Link
          href="/assistant/measures"
          className={`px-3 py-1.5 rounded-full font-medium transition-colors ${
            !area ? "bg-primary text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          Alle
        </Link>
        {areas.map((a) => (
          <Link
            key={a.slug}
            href={`/assistant/measures?area=${a.slug}${status ? `&status=${status}` : ""}`}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium transition-colors ${
              area === a.slug
                ? "bg-primary text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {a.emoji && (
              <i className="material-symbols-outlined md-s">{a.emoji}</i>
            )}
            <span className="leading-none">{a.name}</span>
          </Link>
        ))}
      </div>

      {/* Status filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {[
          { value: undefined, label: "Alle", icon: "filter_list" },
          { value: "OPEN", label: "Offen", icon: "radio_button_unchecked" },
          { value: "IN_PROGRESS", label: "In Bearbeitung", icon: "pending" },
          { value: "DONE", label: "Erledigt", icon: "check_circle" },
          { value: "NOT_APPLICABLE", label: "Nicht zutreffend", icon: "do_not_disturb_on" },
        ].map(({ value, label, icon }) => (
          <Link
            key={label}
            href={`/assistant/measures${area ? `?area=${area}` : ""}${
              value ? `${area ? "&" : "?"}status=${value}` : ""
            }`}
            className={`flex items-center gap-1 px-3 py-1 rounded-full font-medium border transition-colors ${
              status === value
                ? "border-primary bg-primary/10 text-primary"
                : "border-gray-200 text-gray-500 hover:border-gray-400"
            }`}
          >
            <i className="material-symbols-outlined md-s filled">{icon}</i>
            <span className="leading-none">{label}</span>
          </Link>
        ))}
      </div>

      <p className="text-gray-500 mb-4">{items.length} Maßnahmen</p>

      <ChecklistTable items={items} />
    </>
  );
}
