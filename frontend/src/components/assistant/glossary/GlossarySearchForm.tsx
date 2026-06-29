"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useRef } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function GlossarySearchForm({ defaultValue }: { defaultValue?: string }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const inputRef = useRef<HTMLInputElement>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const q = inputRef.current?.value.trim() ?? "";
    const params = new URLSearchParams(searchParams?.toString() ?? "");
    if (q) {
      params.set("q", q);
      params.set("page", "1");
    } else {
      params.delete("q");
      params.delete("page");
    }
    router.push(`?${params.toString()}`);
  }

  function handleClear() {
    if (inputRef.current) inputRef.current.value = "";
    const params = new URLSearchParams(searchParams?.toString() ?? "");
    params.delete("q");
    params.delete("page");
    router.push(`?${params.toString()}`);
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 max-w-xl">
      <Input
        ref={inputRef}
        defaultValue={defaultValue}
        placeholder="Begriff suchen…"
        className="flex-1"
      />
      <Button type="submit">Suchen</Button>
      {defaultValue && (
        <Button type="button" variant="outline" onClick={handleClear}>
          Zurücksetzen
        </Button>
      )}
    </form>
  );
}
