import BackgroundPanel from "@/components/assistant/shared/BackgroundPanel";

const Projektbeschreibung = () => {
  return (
    <BackgroundPanel contentClassName="p-10 md:ps-20">
      <div className="space-y-10 max-w-[85ch]">

        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Über das Projekt</h2>
          <p>
            Die <span className="font-medium">Initiative Cybersicherheit Handwerk</span> ist
            eine digitale Plattform, die Handwerksbetrieben dabei hilft, ihre IT-Sicherheit
            strukturiert zu verbessern. Ziel ist es, auch ohne tiefgreifende IT-Kenntnisse
            einen klaren Überblick über den eigenen Sicherheitsstatus zu erhalten und
            konkrete Maßnahmen umzusetzen.
          </p>
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Hintergrund</h2>
          <p>
            Kleine und mittlere Unternehmen im Handwerk sind zunehmend Ziel von
            Cyberangriffen. Ob Ransomware, Datenverlust oder kompromittierte
            Kundendaten — die Folgen können existenzbedrohend sein. Gleichzeitig
            fehlt es in vielen Betrieben an Zeit, Budget und Fachpersonal, um sich
            systematisch mit IT-Sicherheit auseinanderzusetzen.
          </p>
          <p>
            Die Initiative Cybersicherheit Handwerk setzt hier an: Sie übersetzt
            anerkannte Sicherheitsstandards in eine verständliche, praxisnahe Sprache
            und macht sie für den Handwerksalltag nutzbar.
          </p>
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Wie es funktioniert</h2>
          <p>
            Die Plattform basiert auf den Maßnahmen des{" "}
            <span className="font-medium">BSI IT-Grundschutz</span> — dem anerkannten
            deutschen Standard für Informationssicherheit. Diese Maßnahmen wurden
            für den Einsatz im Handwerk aufbereitet und in vier praxisnahe
            Handlungsbereiche gegliedert:
          </p>
          <ul className="list-disc list-inside space-y-1 text-gray-700 pl-2">
            <li><span className="font-medium">Mensch &amp; Organisation</span> — Schulungen, Rollen und Verantwortlichkeiten</li>
            <li><span className="font-medium">Technik &amp; Systeme</span> — Hardware, Software, Netzwerk und Cloud</li>
            <li><span className="font-medium">Sicherheit &amp; Zugang</span> — Zugriffsrechte, Passwörter und Identitätsmanagement</li>
            <li><span className="font-medium">Risiko &amp; Notfall</span> — Backup, Notfallplanung und Incident Response</li>
          </ul>
          <p>
            Anhand einer interaktiven Checkliste können Betriebe ihren Fortschritt
            verfolgen, Maßnahmen als erledigt markieren und den Sicherheitsstatus
            in der Übersicht ablesen.
          </p>
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Zielgruppe</h2>
          <p>
            Die Plattform richtet sich an Handwerksbetriebe jeder Größe — vom
            Einzelunternehmer bis zum Betrieb mit mehreren Standorten. Vorkenntnisse
            im Bereich IT-Sicherheit sind nicht erforderlich.
          </p>
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Hinweis zur Demo-Version</h2>
          <p className="bg-highlight-50 text-tc-contrast p-4">
            Diese Version ist eine Demo-Instanz der Plattform. Die angezeigten
            Maßnahmen und Inhalte dienen zu Demonstrationszwecken. Es wird keine
            Garantie für Vollständigkeit oder Aktualität der Daten übernommen.
          </p>
        </div>

      </div>
    </BackgroundPanel>
  );
};

export default Projektbeschreibung;