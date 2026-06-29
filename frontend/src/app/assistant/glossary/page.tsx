import CategoryOverview from "@/components/assistant/glossary/CategoryOverview";
import GlossarSearchResults from "@/components/assistant/glossary/GlossarSearchResults";
import GlossarySearchForm from "@/components/assistant/glossary/GlossarySearchForm";
import { searchEntries } from "@/lib/api/glossary.api";
import { Suspense } from "react";

export default async function GlossaryPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; page?: string }>;
}) {
  const { q, page } = await searchParams;
  const currentPage = parseInt(page ?? "1", 10) || 1;

  const searchResults =
    q && q.trim()
      ? await searchEntries({ query: q.trim(), page: currentPage, limit: 20 })
      : undefined;

  return (
    <div className="flex flex-col gap-8">
      <Suspense>
        <GlossarySearchForm defaultValue={q} />
      </Suspense>

      {searchResults ? (
        <GlossarSearchResults searchResults={searchResults} />
      ) : (
        <CategoryOverview />
      )}
    </div>
  );
}
