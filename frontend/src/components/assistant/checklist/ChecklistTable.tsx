"use client";

import { useState, useTransition, useMemo } from "react";
import { toast } from "sonner";
import { ChecklistItem } from "@/lib/api/checklist.api";
import { updateProgress } from "@/lib/actions/progress.action";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

type Status = "OPEN" | "IN_PROGRESS" | "DONE" | "NOT_APPLICABLE";
type SortKey = "id" | "title" | "effort" | "status";
type SortDir = "asc" | "desc";

const STATUS_LABELS: Record<Status, string> = {
  OPEN: "Offen",
  IN_PROGRESS: "In Bearbeitung",
  DONE: "Erledigt",
  NOT_APPLICABLE: "Nicht zutreffend",
};

const STATUS_ICONS: Record<Status, string> = {
  OPEN: "radio_button_unchecked",
  IN_PROGRESS: "pending",
  DONE: "check_circle",
  NOT_APPLICABLE: "do_not_disturb_on",
};

const STATUS_ORDER: Record<Status, number> = {
  OPEN: 0,
  IN_PROGRESS: 1,
  DONE: 2,
  NOT_APPLICABLE: 3,
};

const STATUS_COLORS: Record<Status, string> = {
  OPEN: "bg-gray-100 text-gray-600",
  IN_PROGRESS: "bg-yellow-100 text-yellow-700",
  DONE: "bg-green-100 text-green-700",
  NOT_APPLICABLE: "bg-gray-100 text-gray-400 line-through",
};

const EFFORT_LABELS = ["–", "Sehr gering", "Gering", "Mittel", "Hoch", "Sehr hoch"];

const EFFORT_COLORS = [
  "text-gray-400",                                   // 0 – nicht bewertet
  "bg-green-100 text-green-700",                     // 1 – Sehr gering
  "bg-lime-100 text-lime-700",                       // 2 – Gering
  "bg-yellow-100 text-yellow-700",                   // 3 – Mittel
  "bg-orange-100 text-orange-700",                   // 4 – Hoch
  "bg-red-100 text-red-700",                         // 5 – Sehr hoch
];

function SortIcon({ active, dir }: { active: boolean; dir: SortDir }) {
  if (!active)
    return <i className="material-symbols-outlined md-s opacity-30 select-none">unfold_more</i>;
  return (
    <i className="material-symbols-outlined md-s select-none">
      {dir === "asc" ? "arrow_upward" : "arrow_downward"}
    </i>
  );
}

function SortableHeader({
  label,
  sortKey,
  current,
  dir,
  onSort,
  className,
}: {
  label: string;
  sortKey: SortKey;
  current: SortKey;
  dir: SortDir;
  onSort: (key: SortKey) => void;
  className?: string;
}) {
  return (
    <button
      onClick={() => onSort(sortKey)}
      className={`flex items-center gap-0.5 hover:text-gray-800 transition-colors ${className ?? ""}`}
    >
      {label}
      <SortIcon active={current === sortKey} dir={dir} />
    </button>
  );
}

function StatusSelect({ itemId, current }: { itemId: string; current: Status }) {
  const [isPending, startTransition] = useTransition();

  const handleChange = (newStatus: Status) => {
    startTransition(() => {
      void updateProgress(itemId, newStatus).then((result) => {
        if (!result.success) toast.error(result.error ?? "Status konnte nicht gespeichert werden.");
      });
    });
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          disabled={isPending}
          className={`flex items-center gap-1 rounded-full px-2.5 py-0.5 text-sm font-medium cursor-pointer ${STATUS_COLORS[current]} ${isPending ? "opacity-50" : ""}`}
        >
          <i className="material-symbols-outlined md-xs filled leading-none">{STATUS_ICONS[current]}</i>
          <span>{STATUS_LABELS[current]}</span>
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="min-w-[180px]">
        {(Object.keys(STATUS_LABELS) as Status[]).map((s) => (
          <DropdownMenuItem
            key={s}
            onClick={() => handleChange(s)}
            className={`flex items-center gap-2 cursor-pointer ${s === current ? "font-semibold" : ""}`}
          >
            <i className="material-symbols-outlined md-xs filled leading-none">{STATUS_ICONS[s]}</i>
            {STATUS_LABELS[s]}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

const PAGE_SIZE = 25;

export default function ChecklistTable({ items }: { items: ChecklistItem[] }) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("id");
  const [sortDir, setSortDir] = useState<SortDir>("asc");
  const [page, setPage] = useState(1);

  const handleSort = (key: SortKey) => {
    if (key === sortKey) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
    setPage(1);
  };

  const sorted = useMemo(() => {
    return [...items].sort((a, b) => {
      let cmp = 0;
      switch (sortKey) {
        case "id":
          cmp = a.measure.control_id.localeCompare(b.measure.control_id, undefined, { numeric: true });
          break;
        case "title":
          cmp = (a.short_description ?? a.measure.title).localeCompare(
            b.short_description ?? b.measure.title,
            "de"
          );
          break;
        case "effort":
          cmp = a.measure.effort_level - b.measure.effort_level;
          break;
        case "status":
          cmp = STATUS_ORDER[a.status] - STATUS_ORDER[b.status];
          break;
      }
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [items, sortKey, sortDir]);

  const totalPages = Math.ceil(sorted.length / PAGE_SIZE);
  const paginated = sorted.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  if (items.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-gray-300 p-10 text-center text-gray-500">
        Keine Maßnahmen gefunden.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {/* column headers — hidden on mobile */}
      <div className="hidden sm:flex items-center gap-4 px-5 py-2 text-sm font-semibold text-gray-500 uppercase tracking-wide select-none">
        <span className="shrink-0 w-6" /> {/* chevron placeholder */}
        <SortableHeader label="ID" sortKey="id" current={sortKey} dir={sortDir} onSort={handleSort} className="w-28 shrink-0" />
        <SortableHeader label="Maßnahme" sortKey="title" current={sortKey} dir={sortDir} onSort={handleSort} className="flex-1" />
        <SortableHeader label="Aufwand" sortKey="effort" current={sortKey} dir={sortDir} onSort={handleSort} className="shrink-0 w-28 justify-end" />
        <SortableHeader label="Status" sortKey="status" current={sortKey} dir={sortDir} onSort={handleSort} className="shrink-0 w-40 justify-end" />
      </div>

      {paginated.map((item) => (
        <div key={item.id} className="rounded-lg border border-gray-200 bg-white overflow-hidden">
          <div
            className="flex items-center gap-3 px-3 py-3 sm:gap-4 sm:px-5 sm:py-4 cursor-pointer hover:bg-gray-50"
            onClick={() => setExpanded(expanded === item.id ? null : item.id)}
          >
            {/* expand chevron */}
            <i className="material-symbols-outlined md-m text-gray-300 shrink-0 transition-transform duration-150"
              style={{ transform: expanded === item.id ? "rotate(90deg)" : "rotate(0deg)" }}>
              chevron_right
            </i>

            {/* control id — hidden on mobile */}
            <span className="hidden sm:block shrink-0 font-mono text-gray-400 w-28">
              {item.measure.control_id}
            </span>

            {/* description */}
            <div className="flex-1 min-w-0">
              <p className="font-medium text-gray-800 leading-snug">
                {item.short_description ?? item.measure.title}
              </p>
              {item.measure.parent_control_id && (
                <p className="text-sm text-gray-400 mt-0.5">
                  Unter-Maßnahme von {item.measure.parent_control_id}
                </p>
              )}
              {/* effort badge — visible only on mobile */}
              {item.measure.effort_level > 0 && (
                <span className={`sm:hidden inline-flex mt-1 text-sm rounded-full px-2 py-0.5 font-medium ${EFFORT_COLORS[item.measure.effort_level]}`}>
                  {EFFORT_LABELS[item.measure.effort_level]}
                </span>
              )}
            </div>

            {/* effort — hidden on mobile */}
            <span className={`hidden sm:inline-flex shrink-0 text-sm w-28 text-center justify-center rounded-full px-2 py-0.5 font-medium ${EFFORT_COLORS[item.measure.effort_level]}`}>
              {EFFORT_LABELS[item.measure.effort_level]}
            </span>

            {/* status */}
            <div className="shrink-0 sm:w-40 flex justify-end" onClick={(e) => e.stopPropagation()}>
              <StatusSelect itemId={item.id} current={item.status} />
            </div>
          </div>

          {/* expanded detail */}
          {expanded === item.id && (
            <div className="border-t border-gray-100 px-4 py-3 bg-gray-50 text-sm text-gray-700 space-y-2">
              <p className="font-medium text-gray-600">{item.measure.title}</p>
              <p>{item.measure.requirement_text}</p>
              {item.measure.guidance_text && (
                <details className="text-sm text-gray-500">
                  <summary className="cursor-pointer font-medium underline">Umsetzungshinweis</summary>
                  <p className="mt-1 whitespace-pre-wrap">{item.measure.guidance_text}</p>
                </details>
              )}
              {item.comment_count > 0 && (
                <p className="text-sm text-gray-400">{item.comment_count} Kommentar(e)</p>
              )}
            </div>
          )}
        </div>
      ))}

      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-4">
          <p className="text-sm text-gray-500">
            {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, sorted.length)} von {sorted.length}
          </p>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setPage(1)}
              disabled={page === 1}
              className="p-1.5 rounded text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              aria-label="Erste Seite"
            >
              <i className="material-symbols-outlined md-s">first_page</i>
            </button>
            <button
              onClick={() => setPage((p) => p - 1)}
              disabled={page === 1}
              className="p-1.5 rounded text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              aria-label="Vorherige Seite"
            >
              <i className="material-symbols-outlined md-s">chevron_left</i>
            </button>
            {Array.from({ length: totalPages }, (_, i) => i + 1)
              .filter((p) => p === 1 || p === totalPages || Math.abs(p - page) <= 1)
              .reduce<(number | "…")[]>((acc, p, idx, arr) => {
                if (idx > 0 && p - (arr[idx - 1] as number) > 1) acc.push("…");
                acc.push(p);
                return acc;
              }, [])
              .map((p, idx) =>
                p === "…" ? (
                  <span key={`ellipsis-${idx}`} className="px-2 text-gray-400 text-sm">…</span>
                ) : (
                  <button
                    key={p}
                    onClick={() => setPage(p as number)}
                    className={`min-w-[32px] h-8 px-2 rounded text-sm font-medium transition-colors ${
                      page === p
                        ? "bg-primary text-white"
                        : "text-gray-600 hover:bg-gray-100"
                    }`}
                  >
                    {p}
                  </button>
                )
              )}
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={page === totalPages}
              className="p-1.5 rounded text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              aria-label="Nächste Seite"
            >
              <i className="material-symbols-outlined md-s">chevron_right</i>
            </button>
            <button
              onClick={() => setPage(totalPages)}
              disabled={page === totalPages}
              className="p-1.5 rounded text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
              aria-label="Letzte Seite"
            >
              <i className="material-symbols-outlined md-s">last_page</i>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
