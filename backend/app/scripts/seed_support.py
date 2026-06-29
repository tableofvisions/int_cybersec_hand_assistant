"""Seed support service entries with representative data."""
import uuid

from app.database import SessionLocal
from app.models.support import SupportOffer, SupportOrganization, SupportServiceEntry, SupportTopic

_TOPICS = [
    {"name": "IT-Sicherheitsstrategie", "description": "Aufbau und Weiterentwicklung einer unternehmensweiten IT-Sicherheitsstrategie"},
    {"name": "Risikomanagement", "description": "Identifikation, Bewertung und Behandlung von IT-Sicherheitsrisiken"},
    {"name": "BSI IT-Grundschutz", "description": "Umsetzung des BSI IT-Grundschutz-Kompendiums"},
    {"name": "Datenschutz & DSGVO", "description": "Anforderungen aus der Datenschutz-Grundverordnung"},
    {"name": "Awareness & Schulung", "description": "Sensibilisierung und Schulung von Mitarbeitenden"},
    {"name": "Incident Response", "description": "Vorbereitung auf und Reaktion bei IT-Sicherheitsvorfällen"},
    {"name": "Notfallmanagement", "description": "Business Continuity und IT-Notfallplanung"},
    {"name": "Netzwerksicherheit", "description": "Absicherung von Netzwerkinfrastrukturen"},
    {"name": "Cloud-Sicherheit", "description": "Sichere Nutzung von Cloud-Diensten"},
    {"name": "Penetrationstest", "description": "Sicherheitsüberprüfung durch gezielte Angriffssimulation"},
    {"name": "Phishing & Social Engineering", "description": "Schutz vor manipulativen Angriffsmethoden"},
    {"name": "Zertifizierung", "description": "Vorbereitung und Begleitung von Sicherheitszertifizierungen"},
]

_ORGS = [
    {
        "name": "BSI – Bundesamt für Sicherheit in der Informationstechnik",
        "website": "https://www.bsi.bund.de",
        "mail": "bsi@bsi.bund.de",
        "description": "Nationale Cybersicherheitsbehörde Deutschlands.",
    },
    {
        "name": "Allianz für Cyber-Sicherheit",
        "website": "https://www.allianz-fuer-cybersicherheit.de",
        "description": "Initiative des BSI zur Stärkung der Cyber-Sicherheit in Deutschland.",
    },
    {
        "name": "eco – Verband der Internetwirtschaft e.V.",
        "website": "https://www.eco.de",
        "mail": "info@eco.de",
        "description": "Größter Verband der Internetwirtschaft in Europa.",
    },
    {
        "name": "Handwerkskammer (ZDH) – IT-Sicherheitsberatung",
        "website": "https://cybersicherheit-handwerk.de",
        "description": "IT-Sicherheitsangebote für Handwerksbetriebe über die Zentralorganisation des Handwerks.",
    },
    {
        "name": "Industrie- und Handelskammer (IHK)",
        "website": "https://www.ihk.de/daten-und-informationssicherheit",
        "description": "Beratungs- und Schulungsangebote für Unternehmen im IHK-Netzwerk.",
    },
    {
        "name": "Deutschland sicher im Netz e.V. (DsiN)",
        "website": "https://www.sicher-im-netz.de",
        "mail": "info@sicher-im-netz.de",
        "description": "Gemeinnütziger Verein zur Förderung der digitalen Sicherheitskompetenz.",
    },
    {
        "name": "Cyberwehr Baden-Württemberg",
        "website": "https://cyberwehr-bw.de",
        "phone": "0800 888 7663",
        "description": "Kostenfreier Erst-Hilfe-Dienst für KMU und Kommunen in Baden-Württemberg bei Cyberangriffen.",
    },
]

_ENTRIES = [
    {
        "org": "BSI – Bundesamt für Sicherheit in der Informationstechnik",
        "offer": {
            "name": "IT-Grundschutz-Beratung",
            "description": "Das BSI unterstützt Unternehmen bei der Umsetzung des IT-Grundschutz-Kompendiums mit Leitfäden, Werkzeugen und Beratungsangeboten.",
            "type": "CONSULTATION",
            "topics": ["BSI IT-Grundschutz", "IT-Sicherheitsstrategie", "Zertifizierung"],
        },
        "website": "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/it-grundschutz_node.html",
    },
    {
        "org": "BSI – Bundesamt für Sicherheit in der Informationstechnik",
        "offer": {
            "name": "Cyber-Sicherheits-Check",
            "description": "Strukturierte Überprüfung des IT-Sicherheitsniveaus eines Unternehmens anhand des BSI-Standards 200-1.",
            "type": "CONSULTATION",
            "topics": ["IT-Sicherheitsstrategie", "Risikomanagement"],
        },
        "website": "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Cyber-Sicherheits-Check/cyber-sicherheits-check_node.html",
    },
    {
        "org": "Allianz für Cyber-Sicherheit",
        "offer": {
            "name": "Mitgliedschaft Allianz für Cyber-Sicherheit",
            "description": "Zugang zu Lageberichten, Handlungsempfehlungen und einem Netzwerk von über 7.000 Institutionen. Kostenfreie Mitgliedschaft für Unternehmen.",
            "type": "INFO",
            "topics": ["IT-Sicherheitsstrategie", "Incident Response"],
        },
        "website": "https://www.allianz-fuer-cybersicherheit.de/ACS/DE/Mitmachen/mitmachen.html",
    },
    {
        "org": "Deutschland sicher im Netz e.V. (DsiN)",
        "offer": {
            "name": "SicherheitsCheck für Unternehmen",
            "description": "Kostenfreies Online-Tool zur Selbsteinschätzung des IT-Sicherheitsstands in kleinen und mittleren Unternehmen.",
            "type": "INFO",
            "topics": ["IT-Sicherheitsstrategie", "Risikomanagement", "Awareness & Schulung"],
        },
        "website": "https://www.sicher-im-netz.de/sicherheitscheck",
    },
    {
        "org": "Deutschland sicher im Netz e.V. (DsiN)",
        "offer": {
            "name": "DsiN-Sicherheitsnavigator",
            "description": "Regelmäßige Studie zur IT-Sicherheitslage in kleinen und mittleren Unternehmen mit konkreten Handlungsempfehlungen.",
            "type": "INFO",
            "topics": ["IT-Sicherheitsstrategie", "Awareness & Schulung"],
        },
        "website": "https://www.sicher-im-netz.de/navigator",
    },
    {
        "org": "Handwerkskammer (ZDH) – IT-Sicherheitsberatung",
        "offer": {
            "name": "IT-Sicherheitsbotschafter im Handwerk",
            "description": "Geschulte Ansprechpartner in Handwerkskammern, die Betriebe bei der Umsetzung von IT-Sicherheitsmaßnahmen unterstützen.",
            "type": "CONSULTATION",
            "topics": ["IT-Sicherheitsstrategie", "BSI IT-Grundschutz", "Awareness & Schulung"],
        },
        "website": "https://cybersicherheit-handwerk.de/Sicherheitsbotschafter",
    },
    {
        "org": "Handwerkskammer (ZDH) – IT-Sicherheitsberatung",
        "offer": {
            "name": "Fachberatung IT-Sicherheit für Handwerksbetriebe",
            "description": "Individuelle Beratung durch zertifizierte IT-Sicherheitsfachberater für Handwerksbetriebe.",
            "type": "CONSULTATION",
            "topics": ["IT-Sicherheitsstrategie", "Netzwerksicherheit", "Datenschutz & DSGVO"],
        },
        "website": "https://cybersicherheit-handwerk.de/cgi-bin/scgi?sid=1&se=1&kd=0&sp=deu&rid=179&bef=neueseite",
    },
    {
        "org": "Industrie- und Handelskammer (IHK)",
        "offer": {
            "name": "IHK-Beratung zu Datenschutz und IT-Sicherheit",
            "description": "Erstberatung und Orientierungshilfe für IHK-Mitgliedsunternehmen zu Datenschutz, DSGVO und IT-Sicherheitsanforderungen.",
            "type": "CONSULTATION",
            "topics": ["Datenschutz & DSGVO", "IT-Sicherheitsstrategie"],
        },
        "website": "https://www.ihk.de/daten-und-informationssicherheit",
    },
    {
        "org": "Industrie- und Handelskammer (IHK)",
        "offer": {
            "name": "IHK-Veranstaltungen IT-Sicherheit",
            "description": "Regelmäßige Informationsveranstaltungen, Webinare und Workshops zu aktuellen IT-Sicherheitsthemen.",
            "type": "INFO",
            "topics": ["IT-Sicherheitsstrategie", "Awareness & Schulung", "Phishing & Social Engineering"],
        },
        "website": "https://www.ihk.de/daten-und-informationssicherheit",
    },
    {
        "org": "eco – Verband der Internetwirtschaft e.V.",
        "offer": {
            "name": "eco Schulungsprogramm IT-Sicherheit",
            "description": "Praxisnahe Schulungen und Zertifizierungen zu IT-Sicherheitsthemen für Fachkräfte und Führungskräfte.",
            "type": "TRAINING",
            "topics": ["Awareness & Schulung", "Netzwerksicherheit", "Cloud-Sicherheit"],
        },
        "website": "https://www.eco.de/themen/sicherheit/",
    },
    {
        "org": "Cyberwehr Baden-Württemberg",
        "offer": {
            "name": "Notfall-Hotline bei Cyberangriffen",
            "description": "Kostenfreier telefonischer Ersthelfer-Dienst für KMU in Baden-Württemberg: Soforthilfe und Erstberatung im Cybernotfall.",
            "type": "CONSULTATION",
            "topics": ["Incident Response", "Notfallmanagement"],
        },
        "website": "https://cyberwehr-bw.de",
    },
    {
        "org": "BSI – Bundesamt für Sicherheit in der Informationstechnik",
        "offer": {
            "name": "Digitaler Ersthelfer (BSI-Zertifizierung)",
            "description": "Netzwerk zertifizierter Ersthelfer, die KMU schnell und unbürokratisch bei einem IT-Sicherheitsvorfall unterstützen.",
            "type": "CONSULTATION",
            "topics": ["Incident Response", "Notfallmanagement"],
        },
        "website": "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Cyber-Sicherheitsnetzwerk/Qualifizierung/Digitaler_Ersthelfer/digitaler-ersthelfer_node.html",
    },
    {
        "org": "Deutschland sicher im Netz e.V. (DsiN)",
        "offer": {
            "name": "DsiN-Praxisleitfäden",
            "description": "Kostenfreie Leitfäden zu IT-Sicherheitsthemen speziell für kleine Unternehmen und Vereine, z. B. zu Phishing, Passwörtern und Cloud-Nutzung.",
            "type": "INFO",
            "topics": ["Phishing & Social Engineering", "Cloud-Sicherheit", "Awareness & Schulung"],
        },
        "website": "https://www.sicher-im-netz.de/praxisleitfaeden",
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(SupportServiceEntry).count() > 0:
            print("Support service seed data already present – skipping.")
            return

        topic_map: dict[str, SupportTopic] = {}
        for t in _TOPICS:
            topic = SupportTopic(id=str(uuid.uuid4()), name=t["name"], description=t["description"])
            db.add(topic)
            topic_map[t["name"]] = topic

        org_map: dict[str, SupportOrganization] = {}
        for o in _ORGS:
            org = SupportOrganization(
                id=str(uuid.uuid4()),
                name=o["name"],
                website=o.get("website"),
                phone=o.get("phone"),
                mail=o.get("mail"),
                description=o.get("description"),
            )
            db.add(org)
            org_map[o["name"]] = org

        db.flush()

        for e in _ENTRIES:
            o = e["offer"]
            offer = SupportOffer(
                id=str(uuid.uuid4()),
                name=o["name"],
                description=o["description"],
                type=o["type"],
                topics=[topic_map[t] for t in o["topics"] if t in topic_map],
            )
            db.add(offer)
            db.flush()

            entry = SupportServiceEntry(
                id=str(uuid.uuid4()),
                offer_id=offer.id,
                organization_id=org_map[e["org"]].id,
                website=e.get("website"),
            )
            db.add(entry)

        db.commit()
        print(f"Support service seed data inserted ({len(_ENTRIES)} entries).")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
