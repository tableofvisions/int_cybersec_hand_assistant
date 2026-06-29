import EmergencyContactPanel from "@/components/assistant/incidents/EmergencyContactPanel";
import IncidentSignsPanel from "@/components/assistant/incidents/IncidentSignsPanel";
import LinkListPanel from "@/components/assistant/incidents/LinkListPanel";
import ReportPanel from "@/components/assistant/incidents/ReportPanel";
import StepByStepPanel from "@/components/assistant/incidents/StepByStepPanel";
import Header from "@/components/assistant/shared/Header";
import {
  getIncidentLinks,
  getIncidentSigns,
  getIncidentSteps,
} from "@/lib/api/incidents.api";

export default async function IncidentsPage() {
  const [signs, steps, linkCategories] = await Promise.all([
    getIncidentSigns(),
    getIncidentSteps(),
    getIncidentLinks(),
  ]);

  return (
    <div>
      <Header title="Sicherheitsvorfälle" />
      <div className="grid grid-cols-12 gap-4">
        <EmergencyContactPanel className="col-span-12" />
        <IncidentSignsPanel
          className="col-span-12 lg:col-span-6"
          signs={signs}
        />
        <StepByStepPanel
          className="col-span-12 lg:col-span-6"
          steps={steps}
        />
        <ReportPanel className="col-span-12" />
        <LinkListPanel
          className="col-span-12"
          categories={linkCategories}
        />
      </div>
    </div>
  );
}
