import { cn } from "@/lib/utils";
import React from "react";
import IncidentPanel from "./IncidentPanel";
import Link from "next/link";
import { IncidentLinkCategory } from "@/lib/api/incidents.api";

const LinkListPanel = ({
  className,
  categories,
}: {
  className?: string;
  categories: IncidentLinkCategory[];
}) => {
  if (categories.length === 0) return null;

  return (
    <IncidentPanel
      className={cn(className)}
      title="Wo finde ich weitere Informationen?"
    >
      <div className="flex flex-wrap gap-8" id="links">
        {categories.map((category) => {
          if (category.links.length === 0) return null;
          return (
            <div
              key={category.id}
              id={`link_${category.id}`}
              className="w-full lg:w-[45%] bg-contrast-verylight"
            >
              <h4 className="font-semibold w-full bg-highlight-50 text-tc-contrast p-4">
                {category.title}
              </h4>
              <ul className="list-inside p-4 ms-8 space-y-3">
                {category.links.map((link) => (
                  <li key={link.url} className="list-disc leading-snug">
                    <Link href={link.url} className="external-link" target="_blank">
                      {link.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
      <div className="w-full text-right mt-4">
        Quelle:{" "}
        <Link
          href="https://www.bsi.bund.de/DE/IT-Sicherheitsvorfall/Unternehmen/Ich-habe-einen-IT-Sicherheitsvorfall-Checkliste-Organisatorisches/ich-habe-einen-it-sicherheitsvorfall-checkliste-organisatorisches_node.html"
          className="external-link"
        >
          BSI
        </Link>
      </div>
    </IncidentPanel>
  );
};

export default LinkListPanel;
