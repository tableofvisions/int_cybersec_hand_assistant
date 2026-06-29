import Header from "@/components/assistant/shared/Header";

export default function InfrastructurePage() {
  return (
    <>
      <Header title="IT-Infrastruktur" />
      <ComingSoon description="Die Verwaltung von IT-Komponenten wird in einer späteren Version verfügbar sein." />
    </>
  );
}

function ComingSoon({ description }: { description: string }) {
  return (
    <div className="mt-8 rounded-xl border border-dashed border-gray-300 p-10 text-center text-gray-500">
      <p className="text-lg font-medium">Demnächst verfügbar</p>
      <p className="text-sm mt-1">{description}</p>
    </div>
  );
}
