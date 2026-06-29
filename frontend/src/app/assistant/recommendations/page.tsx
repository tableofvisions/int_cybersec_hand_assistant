import Header from "@/components/assistant/shared/Header";

export default function RecommendationsPage() {
  return (
    <>
      <Header title="Empfehlungen" />
      <div className="mt-8 rounded-xl border border-dashed border-gray-300 p-10 text-center text-gray-500">
        <p className="text-lg font-medium">Demnächst verfügbar</p>
        <p className="text-sm mt-1">Automatische Sicherheitsempfehlungen werden in einer späteren Version verfügbar sein.</p>
      </div>
    </>
  );
}
