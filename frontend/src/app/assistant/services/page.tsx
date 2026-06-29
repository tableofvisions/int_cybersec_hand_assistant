import { DataTableColumns } from "@/components/assistant/guidance/DataTableColumns";
import ServicesTable from "@/components/assistant/guidance/ServicesTable";
import Header from "@/components/assistant/shared/Header";
import { getAllEntries } from "@/lib/api/supportServices.api";
import { ServicesTableFacets } from "@/types/assistant";

export default async function ServicesPage() {
  const data = await getAllEntries();

  if (!data) {
    return (
      <>
        <Header title="Unterstützungsangebote" />
        <div className="mt-8 rounded-xl border border-dashed border-gray-300 p-10 text-center text-gray-500">
          <p className="text-lg font-medium">Daten konnten nicht geladen werden.</p>
        </div>
      </>
    );
  }

  const topicNames = Array.from(
    data.reduce((set: Set<string>, entry) => {
      entry.offer?.topics?.forEach((t) => set.add(t.name));
      return set;
    }, new Set<string>())
  ).sort((a, b) => a.localeCompare(b));

  const providerNames = Array.from(
    data.reduce((set: Set<string>, entry) => {
      if (entry.provider?.name) set.add(entry.provider.name);
      return set;
    }, new Set<string>())
  ).sort((a, b) => a.localeCompare(b));

  const offerTypes = Array.from(
    data.reduce((set: Set<string>, entry) => {
      if (entry.offer?.type) set.add(entry.offer.type);
      return set;
    }, new Set<string>())
  ).sort((a, b) => a.localeCompare(b));

  const facets: ServicesTableFacets = [
    { column: "topics", title: "Inhalte", data: topicNames },
    { column: "provider", title: "Anbieter", data: providerNames },
    { column: "type", title: "Angebotstyp", data: offerTypes },
  ];

  return (
    <>
      <Header title="Unterstützungsangebote" />
      <ServicesTable data={data} columns={DataTableColumns} facets={facets} />
    </>
  );
}
