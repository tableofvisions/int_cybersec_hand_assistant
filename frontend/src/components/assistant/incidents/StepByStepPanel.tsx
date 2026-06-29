import { cn } from "@/lib/utils";
import React from "react";
import IncidentPanel from "./IncidentPanel";
import SingleStep from "./SingleStep";
import Link from "next/link";
import { IncidentStep } from "@/lib/api/incidents.api";

const StepByStepPanel = ({
  className,
  steps,
}: {
  className?: string;
  steps: IncidentStep[];
}) => {
  return (
    <IncidentPanel className={cn(className)} title="Was tun im Ernstfall?">
      <div className="space-y-8">
        {steps.map((step) => (
          <SingleStep key={step.pos} pos={step.pos} title={step.title}>
            {step.text}
            {step.sourceUrl && (
              <>
                {" "}
                <Link href={step.sourceUrl} className="external-link" target="_blank">
                  {step.sourceLabel ?? "Weitere Informationen"}
                </Link>
              </>
            )}
          </SingleStep>
        ))}
      </div>
      <div className="w-full text-right mt-4">
        Quelle:{" "}
        <Link
          href="https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Cyber-Sicherheit/Themen/Ransomware_Erste-Hilfe-IT-Sicherheitsvorfall.pdf?__blob=publicationFile&v=3"
          className="external-link"
          target="_blank"
        >
          BSI
        </Link>
      </div>
    </IncidentPanel>
  );
};

export default StepByStepPanel;
