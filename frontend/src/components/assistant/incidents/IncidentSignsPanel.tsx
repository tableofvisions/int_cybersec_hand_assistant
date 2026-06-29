import { cn } from "@/lib/utils";
import React from "react";
import IncidentPanel from "./IncidentPanel";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Separator } from "@/components/ui/separator";
import IncidentSignsKnowledgeWrapper from "./IncidentSignsKnowledgeWrapper";
import { IncidentSign } from "@/lib/api/incidents.api";

const IncidentSignsPanel = ({
  className,
  signs,
}: {
  className?: string;
  signs: IncidentSign[];
}) => {
  return (
    <IncidentPanel
      className={cn(className)}
      title="Woran erkenne ich einen IT-Sicherheitsvorfall?"
    >
      <div className="space-y-4">
        <p>Wenn Sie eines dieser Anzeichen bemerken, sollten Sie sofort handeln!</p>
        <Accordion type="single" collapsible>
          {signs.map((sign) => (
            <AccordionItem key={sign.id} value={sign.id} className="border-0 mb-2">
              <AccordionTrigger className="text-base text-left font-semibold bg-contrast-light p-4 data-[state=open]:bg-highlight-50 data-[state=open]:text-tc-contrast">
                {sign.title}
              </AccordionTrigger>
              <AccordionContent className="text-base bg-background p-4 border-s-4 border-contrast-light">
                <p className="mb-4">{sign.description}</p>
                <h4 className="font-semibold">Beispiele:</h4>
                <ul className="list-inside ms-6">
                  {sign.examples.map((example, index) => (
                    <li key={index} className="list-disc">
                      {example}
                    </li>
                  ))}
                </ul>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
      <Separator className="my-6" />
      <IncidentSignsKnowledgeWrapper />
    </IncidentPanel>
  );
};

export default IncidentSignsPanel;
