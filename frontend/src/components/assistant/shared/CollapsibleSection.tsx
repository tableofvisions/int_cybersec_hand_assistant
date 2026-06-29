"use client";

import { useState, useEffect, useRef } from "react";

export default function CollapsibleSection({
  title,
  storageKey,
  defaultOpen = true,
  headerExtra,
  children,
}: {
  title: string;
  storageKey: string;
  defaultOpen?: boolean;
  headerExtra?: React.ReactNode;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const initialized = useRef(false);

  useEffect(() => {
    const stored = localStorage.getItem(storageKey);
    if (stored !== null) setOpen(stored === "true");
    initialized.current = true;
  }, [storageKey]);

  const toggle = () => {
    const next = !open;
    setOpen(next);
    localStorage.setItem(storageKey, String(next));
  };

  return (
    <section className="mt-10">
      <div className="flex items-center justify-between mb-3">
        <button
          onClick={toggle}
          className="flex items-center gap-1.5 group"
        >
          <i
            className="material-symbols-outlined md-l text-gray-400 transition-transform duration-200"
            style={{ transform: open ? "rotate(90deg)" : "rotate(0deg)" }}
          >
            chevron_right
          </i>
          <h2 className="font-semibold text-gray-900 group-hover:text-gray-700 hyphens-auto">
            {title}
          </h2>
        </button>
        {headerExtra}
      </div>
      {open && <div>{children}</div>}
    </section>
  );
}
