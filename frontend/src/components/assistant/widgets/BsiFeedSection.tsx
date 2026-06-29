import { CommonSecurityAdvisoryFramework } from "@/types/csaf";
import WarningTickerItem from "./WarningTickerItem";

const CERT_BUND_BASE = "https://wid.cert-bund.de/.well-known/csaf/white";

async function fetchBsiFeed(limit: number): Promise<CommonSecurityAdvisoryFramework[]> {
  try {
    const indexRes = await fetch(`${CERT_BUND_BASE}/index.txt`, {
      next: { revalidate: 3600 },
    });
    if (!indexRes.ok) return [];

    const text = await indexRes.text();
    const paths = text
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean)
      .sort((a, b) => {
        const ma = a.match(/(\d{4})[/-](\d+)/);
        const mb = b.match(/(\d{4})[/-](\d+)/);
        if (!ma || !mb) return 0;
        const yearDiff = parseInt(mb[1]) - parseInt(ma[1]);
        return yearDiff !== 0 ? yearDiff : parseInt(mb[2]) - parseInt(ma[2]);
      })
      .slice(0, limit);

    const results = await Promise.allSettled(
      paths.map(async (path) => {
        const url = path.startsWith("http") ? path : `${CERT_BUND_BASE}/${path}`;
        const res = await fetch(url, { next: { revalidate: 3600 } });
        if (!res.ok) throw new Error("fetch failed");
        return res.json() as Promise<CommonSecurityAdvisoryFramework>;
      })
    );

    return results
      .filter((r): r is PromiseFulfilledResult<CommonSecurityAdvisoryFramework> => r.status === "fulfilled")
      .map((r) => r.value);
  } catch {
    return [];
  }
}

export default async function BsiFeedSection() {
  const advisories = await fetchBsiFeed(15);

  return (
    <div className="rounded-xl border border-gray-200 bg-white overflow-hidden">
      {advisories.length === 0 ? (
        <p className="px-4 py-6 text-gray-400 text-center">Keine Warnungen verfügbar</p>
      ) : (
        <div className="divide-y divide-gray-100">
          {advisories.map((csa, i) => (
            <WarningTickerItem key={i} csa={csa} />
          ))}
        </div>
      )}
      <div className="px-4 py-3 border-t border-gray-100 text-gray-400 flex flex-wrap items-center justify-between gap-2">
        <span>
          Quelle:{" "}
          <a
            href="https://wid.cert-bund.de"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:text-gray-600"
          >
            CERT-Bund
          </a>{" "}
          · Aktualisierung stündlich
        </span>
        <a
          href="https://wid.cert-bund.de"
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary hover:underline flex items-center gap-1"
        >
          Alle Warnungen anzeigen
          <i className="material-symbols-outlined md-xs">open_in_new</i>
        </a>
      </div>
    </div>
  );
}
