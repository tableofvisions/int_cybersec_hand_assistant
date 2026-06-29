"""Seed the glossary with German IT-security terminology."""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from app.database import SessionLocal
from app.models.glossary import GlossaryCategory, GlossaryReference, GlossarySource, GlossarySynonym, GlossaryTerm


CATEGORIES = [
    {
        "name": "Grundlagen",
        "description": "Grundlegende Konzepte und Begriffe der Informationssicherheit",
        "image_src": "/assets/images/glossary/hero/shield.hero.svg",
    },
    {
        "name": "Netzwerk & Infrastruktur",
        "description": "Begriffe rund um Netzwerke, Protokolle und IT-Infrastruktur",
        "image_src": "/assets/images/glossary/hero/commandline.hero.svg",
    },
    {
        "name": "Zugang & Identität",
        "description": "Authentifizierung, Autorisierung und Identitätsmanagement",
        "image_src": "/assets/images/glossary/hero/default.svg",
    },
    {
        "name": "Bedrohungen & Angriffe",
        "description": "Arten von Cyberangriffen, Schadsoftware und Bedrohungsakteure",
        "image_src": "/assets/images/glossary/hero/shield.hero.svg",
    },
    {
        "name": "Schutzmaßnahmen",
        "description": "Technische und organisatorische Maßnahmen zum Schutz von Systemen",
        "image_src": "/assets/images/glossary/hero/default.svg",
    },
    {
        "name": "Compliance & Recht",
        "description": "Gesetzliche Anforderungen, Normen und Datenschutz",
        "image_src": "/assets/images/glossary/hero/shield.hero.svg",
    },
]

TERMS = {
    "Grundlagen": [
        {
            "keyword": "Informationssicherheit",
            "definition": "Schutz von Informationen vor unbefugtem Zugriff, Veränderung und Verlust.",
            "description": (
                "Informationssicherheit umfasst alle Maßnahmen zum Schutz von Informationen in Bezug auf "
                "Vertraulichkeit, Integrität und Verfügbarkeit (CIA-Triade). Sie schließt sowohl technische "
                "als auch organisatorische Aspekte ein und ist nicht auf IT-Systeme beschränkt."
            ),
            "synonyms": ["IT-Sicherheit", "Cybersicherheit"],
            "sources": [
                {"name": "BSI Grundschutz-Kompendium", "url": "https://www.bsi.bund.de/grundschutz"},
                {"name": "ISO/IEC 27001", "url": "https://www.iso.org/standard/27001"},
            ],
        },
        {
            "keyword": "Vertraulichkeit",
            "definition": "Eigenschaft, dass Informationen nur autorisierten Personen zugänglich sind.",
            "description": (
                "Vertraulichkeit stellt sicher, dass sensible Daten nur von Personen eingesehen werden können, "
                "die dazu berechtigt sind. Maßnahmen zur Sicherstellung umfassen Verschlüsselung, "
                "Zugriffskontrollen und Need-to-know-Prinzip."
            ),
            "synonyms": ["Geheimhaltung", "Datenschutz"],
            "sources": [{"name": "ISO/IEC 27000", "url": "https://www.iso.org/standard/73906.html"}],
        },
        {
            "keyword": "Integrität",
            "definition": "Sicherstellung, dass Informationen vollständig und unverändert sind.",
            "description": (
                "Integrität bedeutet, dass Daten während der Übertragung oder Speicherung nicht unautorisiert "
                "verändert werden. Kryptografische Prüfsummen (Hashes) und digitale Signaturen sind typische "
                "Integritätsschutzmechanismen."
            ),
            "synonyms": ["Datentreue", "Unversehrtheit"],
            "sources": [{"name": "BSI IT-Grundschutz", "url": "https://www.bsi.bund.de/grundschutz"}],
        },
        {
            "keyword": "Verfügbarkeit",
            "definition": "Sicherstellung, dass Systeme und Daten für autorisierte Nutzer jederzeit erreichbar sind.",
            "description": (
                "Verfügbarkeit garantiert, dass IT-Systeme und die darin enthaltenen Informationen dann zur "
                "Verfügung stehen, wenn sie benötigt werden. Redundanz, Backup-Systeme und "
                "Notfallwiederherstellungspläne sind typische Maßnahmen."
            ),
            "synonyms": ["Ausfallsicherheit"],
            "sources": [],
        },
        {
            "keyword": "Risikoanalyse",
            "definition": "Systematische Identifikation und Bewertung von Sicherheitsrisiken.",
            "description": (
                "Eine Risikoanalyse identifiziert potenzielle Bedrohungen, bewertet deren Eintrittswahrscheinlichkeit "
                "und mögliche Auswirkungen. Das Ergebnis ist eine Priorisierung von Schutzmaßnahmen auf Basis "
                "des ermittelten Risikos."
            ),
            "synonyms": ["Gefährdungsanalyse", "Bedrohungsanalyse"],
            "sources": [{"name": "ISO/IEC 27005", "url": "https://www.iso.org/standard/80585.html"}],
        },
        {
            "keyword": "Schutzbedarfsfeststellung",
            "definition": "BSI-Methode zur Ermittlung des Schutzbedarfs von IT-Systemen und Informationen.",
            "description": (
                "Im BSI IT-Grundschutz wird der Schutzbedarf in drei Kategorien eingeteilt: normal, hoch und "
                "sehr hoch. Die Einstufung bestimmt, welche Sicherheitsmaßnahmen zu implementieren sind."
            ),
            "synonyms": [],
            "sources": [{"name": "BSI IT-Grundschutz-Kompendium", "url": "https://www.bsi.bund.de/grundschutz"}],
        },
        {
            "keyword": "CIA-Triade",
            "definition": "Modell der drei Kernziele der Informationssicherheit: Vertraulichkeit, Integrität, Verfügbarkeit.",
            "description": (
                "Die CIA-Triade (Confidentiality, Integrity, Availability) ist das grundlegende Sicherheitsmodell "
                "in der Informationssicherheit. Alle Sicherheitsmaßnahmen lassen sich einem oder mehreren dieser "
                "drei Schutzziele zuordnen."
            ),
            "synonyms": ["Schutzziele", "Sicherheitsdreieck"],
            "sources": [],
        },
    ],
    "Netzwerk & Infrastruktur": [
        {
            "keyword": "Firewall",
            "definition": "Sicherheitssystem zur Überwachung und Kontrolle des Netzwerkdatenverkehrs.",
            "description": (
                "Eine Firewall analysiert ein- und ausgehenden Netzwerkverkehr anhand definierter Regeln und "
                "blockiert unerwünschte Verbindungen. Man unterscheidet zwischen Paketfilter-Firewalls, "
                "Stateful-Inspection-Firewalls und Next-Generation-Firewalls (NGFW)."
            ),
            "synonyms": ["Netzwerkschutzwand", "Paketfilter"],
            "sources": [{"name": "BSI-Empfehlungen zur Firewall", "url": "https://www.bsi.bund.de"}],
        },
        {
            "keyword": "VPN",
            "definition": "Virtual Private Network – verschlüsselter Tunnel über ein öffentliches Netzwerk.",
            "description": (
                "Ein VPN ermöglicht sichere Kommunikation über unsichere Netzwerke wie das Internet. "
                "Typische Protokolle sind IPsec, OpenVPN und WireGuard. VPNs werden für Remote-Zugriff und "
                "Site-to-Site-Verbindungen genutzt."
            ),
            "synonyms": ["Virtuelles Privates Netzwerk"],
            "sources": [],
        },
        {
            "keyword": "DMZ",
            "definition": "Demilitarisierte Zone – Netzwerksegment zwischen internem und externem Netz.",
            "description": (
                "Eine DMZ ist ein abgeschirmtes Netzwerksegment, in dem öffentlich zugängliche Server "
                "(z. B. Webserver, Mailserver) platziert werden. Sie trennt das interne Netzwerk vom Internet "
                "und schränkt Angriffsmöglichkeiten ein."
            ),
            "synonyms": ["Demilitarisierte Zone", "Pufferzone"],
            "sources": [],
        },
        {
            "keyword": "IDS/IPS",
            "definition": "Intrusion Detection / Prevention System – erkennt und blockiert Netzwerkangriffe.",
            "description": (
                "Ein IDS erkennt Angriffe und meldet sie, ein IPS kann zusätzlich automatisch reagieren "
                "und Verbindungen blockieren. Beide Systeme analysieren Netzwerkverkehr auf Anomalien "
                "und bekannte Angriffsmuster (Signaturen)."
            ),
            "synonyms": ["Einbruchserkennungssystem", "Angriffserkennung"],
            "sources": [],
        },
        {
            "keyword": "Netzwerksegmentierung",
            "definition": "Aufteilung eines Netzwerks in getrennte Segmente zur Begrenzung von Angriffen.",
            "description": (
                "Durch Segmentierung werden verschiedene Systeme in separate Netzwerkbereiche aufgeteilt. "
                "So kann ein Angreifer, der ein Segment kompromittiert, nicht direkt auf andere Bereiche "
                "zugreifen. VLANs und Firewalls werden zur Segmentierung eingesetzt."
            ),
            "synonyms": ["Netzwerktrennung", "Mikrosegmentierung"],
            "sources": [],
        },
        {
            "keyword": "Zero Trust",
            "definition": "Sicherheitsarchitektur ohne implizites Vertrauen – jede Anfrage wird geprüft.",
            "description": (
                "Zero Trust basiert auf dem Prinzip 'never trust, always verify'. Kein Nutzer oder System "
                "erhält automatisch Vertrauen, auch nicht innerhalb des internen Netzwerks. Jeder Zugriff "
                "wird authentifiziert und autorisiert."
            ),
            "synonyms": ["Zero-Trust-Architektur", "ZTA"],
            "sources": [{"name": "NIST SP 800-207", "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final"}],
        },
    ],
    "Zugang & Identität": [
        {
            "keyword": "Authentifizierung",
            "definition": "Nachweis der Identität eines Nutzers oder Systems.",
            "description": (
                "Authentifizierung überprüft, ob jemand tatsächlich derjenige ist, der er vorgibt zu sein. "
                "Methoden umfassen Wissen (Passwort), Besitz (Token) und Biometrie. Starke Authentifizierung "
                "kombiniert mehrere Faktoren (MFA)."
            ),
            "synonyms": ["Identitätsprüfung", "Identifikation"],
            "sources": [],
        },
        {
            "keyword": "Multi-Faktor-Authentifizierung",
            "definition": "Sicherheitsverfahren mit mindestens zwei unabhängigen Authentifizierungsfaktoren.",
            "description": (
                "MFA erhöht die Sicherheit erheblich, da ein Angreifer neben dem Passwort einen zweiten "
                "Faktor kompromittieren müsste. Typisch sind: Passwort + SMS-Code, Passwort + Hardware-Token "
                "oder Passwort + biometrisches Merkmal."
            ),
            "synonyms": ["MFA", "Zwei-Faktor-Authentifizierung", "2FA"],
            "sources": [{"name": "BSI Empfehlung MFA", "url": "https://www.bsi.bund.de"}],
        },
        {
            "keyword": "Autorisierung",
            "definition": "Prüfung, ob ein authentifizierter Nutzer berechtigt ist, eine Aktion auszuführen.",
            "description": (
                "Nach erfolgreicher Authentifizierung bestimmt die Autorisierung, auf welche Ressourcen "
                "und Aktionen ein Nutzer Zugriff hat. Rollenbasierte Zugriffskontrolle (RBAC) ist ein "
                "verbreitetes Modell."
            ),
            "synonyms": ["Zugriffssteuerung", "Berechtigungsprüfung"],
            "sources": [],
        },
        {
            "keyword": "Prinzip der minimalen Rechtevergabe",
            "definition": "Nutzer und Systeme erhalten nur die Rechte, die sie für ihre Aufgaben benötigen.",
            "description": (
                "Das Least-Privilege-Prinzip reduziert den Schaden bei Kompromittierung eines Kontos, "
                "da Angreifer nur eingeschränkte Rechte erhalten. Es verhindert auch versehentliche "
                "Änderungen an kritischen Systemen."
            ),
            "synonyms": ["Least Privilege", "Minimalprinzip", "Need-to-know"],
            "sources": [],
        },
        {
            "keyword": "Single Sign-On",
            "definition": "Verfahren, bei dem sich Nutzer einmalig anmelden und auf mehrere Dienste zugreifen.",
            "description": (
                "SSO verbessert die Benutzerfreundlichkeit, indem nur eine Anmeldung für mehrere "
                "Anwendungen erforderlich ist. SAML, OAuth 2.0 und OpenID Connect sind gängige Standards. "
                "Sicherheitsrisiko: Ein kompromittiertes Konto ermöglicht Zugriff auf alle verknüpften Dienste."
            ),
            "synonyms": ["SSO", "Einmalanmeldung"],
            "sources": [],
        },
        {
            "keyword": "Privileged Access Management",
            "definition": "Kontrolle und Überwachung von Konten mit erhöhten Berechtigungen.",
            "description": (
                "PAM-Systeme verwalten und überwachen privilegierte Konten (Administratoren, Service-Accounts). "
                "Dazu gehören sichere Passworttresore, Session-Aufzeichnung und zeitlich begrenzte Berechtigungen "
                "(Just-in-Time-Access)."
            ),
            "synonyms": ["PAM", "Privileged Identity Management"],
            "sources": [],
        },
    ],
    "Bedrohungen & Angriffe": [
        {
            "keyword": "Malware",
            "definition": "Oberbegriff für schädliche Software wie Viren, Trojaner und Ransomware.",
            "description": (
                "Malware ist Software, die ohne Wissen des Nutzers schädliche Aktionen ausführt. "
                "Unterarten sind Viren (selbst replizierend), Trojaner (getarnte Schadsoftware), "
                "Ransomware (Verschlüsselung gegen Lösegeld) und Spyware (Datendiebstahl)."
            ),
            "synonyms": ["Schadsoftware", "Schadprogramm"],
            "sources": [],
        },
        {
            "keyword": "Ransomware",
            "definition": "Schadsoftware, die Daten verschlüsselt und Lösegeld für die Entschlüsselung fordert.",
            "description": (
                "Ransomware-Angriffe können ganze Organisationen lahmlegen. Typische Verbreitungswege sind "
                "Phishing-E-Mails und kompromittierte RDP-Verbindungen. Regelmäßige Backups (offline/offsite) "
                "sind der wichtigste Schutz."
            ),
            "synonyms": ["Erpressungstrojaner", "Verschlüsselungstrojaner"],
            "sources": [{"name": "BSI Ransomware-Warnung", "url": "https://www.bsi.bund.de"}],
        },
        {
            "keyword": "Phishing",
            "definition": "Täuschungsversuch, bei dem Angreifer sich als vertrauenswürdige Quelle ausgeben.",
            "description": (
                "Phishing-Angriffe erfolgen meist per E-Mail und verleiten Opfer zur Preisgabe von Zugangsdaten "
                "oder zum Herunterladen von Malware. Spear-Phishing ist gezielt auf bestimmte Personen "
                "ausgerichtet, Whaling zielt auf Führungskräfte."
            ),
            "synonyms": ["Phishing-Angriff", "Social Engineering via E-Mail"],
            "sources": [],
        },
        {
            "keyword": "Social Engineering",
            "definition": "Manipulation von Menschen, um sicherheitsrelevante Informationen zu erlangen.",
            "description": (
                "Social Engineering nutzt psychologische Manipulation statt technischer Mittel. "
                "Methoden sind Phishing, Pretexting (Vortäuschen einer falschen Identität), Baiting "
                "(physische Köder wie USB-Sticks) und Tailgating (physischer Zutritt)."
            ),
            "synonyms": ["Soziale Manipulation", "Menschenhacking"],
            "sources": [],
        },
        {
            "keyword": "DDoS-Angriff",
            "definition": "Distributed Denial of Service – Überlastung eines Dienstes durch massenhafte Anfragen.",
            "description": (
                "Bei einem DDoS-Angriff wird ein Zielserver mit Anfragen von vielen kompromittierten Systemen "
                "(Botnetz) überflutet, sodass er nicht mehr erreichbar ist. Schutzmaßnahmen umfassen "
                "Traffic-Scrubbing und Content Delivery Networks (CDN)."
            ),
            "synonyms": ["Denial-of-Service-Angriff", "DDoS"],
            "sources": [],
        },
        {
            "keyword": "Zero-Day-Schwachstelle",
            "definition": "Sicherheitslücke, für die noch kein Patch des Herstellers existiert.",
            "description": (
                "Zero-Day-Exploits nutzen Schwachstellen aus, bevor der Hersteller sie kennt oder behoben hat. "
                "Sie sind besonders gefährlich, da klassische Patch-Management-Prozesse nicht greifen. "
                "Verhaltensbasierte Erkennung und Sandbox-Technologien können helfen."
            ),
            "synonyms": ["Zero-Day", "0-Day", "Nulltag-Exploit"],
            "sources": [],
        },
        {
            "keyword": "Man-in-the-Middle-Angriff",
            "definition": "Angriff, bei dem ein Angreifer die Kommunikation zwischen zwei Parteien abfängt.",
            "description": (
                "Bei einem MitM-Angriff schaltet sich der Angreifer unbemerkt in die Kommunikation ein "
                "und kann Daten lesen oder manipulieren. ARP-Spoofing, DNS-Spoofing und SSL-Stripping "
                "sind typische Techniken. TLS/HTTPS und HSTS schützen davor."
            ),
            "synonyms": ["MitM", "Lauschangriff"],
            "sources": [],
        },
        {
            "keyword": "APT",
            "definition": "Advanced Persistent Threat – gezielter, dauerhafter Angriff durch hochqualifizierte Angreifer.",
            "description": (
                "APTs sind langfristige Angriffskampagnen, meist durch staatlich gesponserte Akteure oder "
                "organisierte Kriminelle. Sie kombinieren Social Engineering, maßgeschneiderte Malware und "
                "Living-off-the-Land-Techniken, um möglichst lange unentdeckt zu bleiben."
            ),
            "synonyms": ["Fortgeschrittene Bedrohung", "Staatliche Cyberangriffe"],
            "sources": [],
        },
    ],
    "Schutzmaßnahmen": [
        {
            "keyword": "Verschlüsselung",
            "definition": "Umwandlung von Daten in eine für Unbefugte unleserliche Form.",
            "description": (
                "Verschlüsselung schützt Daten vor unbefugtem Zugriff. Man unterscheidet symmetrische "
                "Verschlüsselung (gleicher Schlüssel für Ver- und Entschlüsselung, z. B. AES) und "
                "asymmetrische Verschlüsselung (öffentlicher/privater Schlüssel, z. B. RSA, ECC)."
            ),
            "synonyms": ["Kryptografie", "Chiffrierung"],
            "sources": [{"name": "BSI Kryptografieempfehlungen", "url": "https://www.bsi.bund.de/krypto"}],
        },
        {
            "keyword": "Patch-Management",
            "definition": "Systematischer Prozess zur Aktualisierung und Absicherung von Software.",
            "description": (
                "Patch-Management umfasst das zeitnahe Einspielen von Sicherheitsupdates. "
                "BSI empfiehlt, kritische Patches innerhalb von 72 Stunden einzuspielen. "
                "Ein Vulnerability-Management-System unterstützt die Priorisierung."
            ),
            "synonyms": ["Update-Management", "Schwachstellenbehebung"],
            "sources": [],
        },
        {
            "keyword": "Backup",
            "definition": "Sicherungskopie von Daten zur Wiederherstellung nach Datenverlust.",
            "description": (
                "Die 3-2-1-Backup-Regel empfiehlt: 3 Kopien der Daten, auf 2 unterschiedlichen Medien, "
                "1 davon offsite. Regelmäßige Restore-Tests stellen sicher, dass Backups tatsächlich "
                "funktionieren. Ransomware-Schutz erfordert offline oder unveränderliche Backups."
            ),
            "synonyms": ["Datensicherung", "Sicherungskopie"],
            "sources": [],
        },
        {
            "keyword": "Penetrationstest",
            "definition": "Autorisierter Simulationsangriff zur Aufdeckung von Sicherheitslücken.",
            "description": (
                "Ein Penetrationstest (Pentest) prüft die Sicherheit eines Systems durch kontrollierte "
                "Angriffe. Man unterscheidet Black-Box- (ohne Vorkenntnisse), White-Box- (mit vollständiger "
                "Dokumentation) und Grey-Box-Tests. BSI hat eine Zertifizierung für Pentester."
            ),
            "synonyms": ["Pentest", "Ethical Hacking", "Sicherheitstest"],
            "sources": [{"name": "BSI Leitfaden Penetrationstest", "url": "https://www.bsi.bund.de"}],
        },
        {
            "keyword": "Security Information and Event Management",
            "definition": "System zur zentralen Sammlung, Korrelation und Analyse von Sicherheitsereignissen.",
            "description": (
                "SIEM-Systeme aggregieren Logs aus verschiedenen Quellen (Firewall, Server, Anwendungen) "
                "und erkennen Angriffsmuster durch Korrelation. Sie sind Grundlage für ein Security "
                "Operations Center (SOC) und unterstützen die Incident Response."
            ),
            "synonyms": ["SIEM", "Log-Management", "Sicherheitsinformationssystem"],
            "sources": [],
        },
        {
            "keyword": "Incident Response",
            "definition": "Strukturierter Prozess zur Reaktion auf Sicherheitsvorfälle.",
            "description": (
                "Incident Response umfasst die Phasen: Vorbereitung, Erkennung, Eindämmung, Beseitigung, "
                "Wiederherstellung und Nachbereitung. Ein Incident-Response-Plan sollte regelmäßig geübt "
                "werden (Tabletop-Übungen)."
            ),
            "synonyms": ["Vorfallsreaktion", "Sicherheitsvorfallbehandlung"],
            "sources": [{"name": "BSI Empfehlung Incident Response", "url": "https://www.bsi.bund.de"}],
        },
        {
            "keyword": "Schwachstellenmanagement",
            "definition": "Kontinuierlicher Prozess zur Identifikation und Behebung von Sicherheitslücken.",
            "description": (
                "Schwachstellenmanagement umfasst regelmäßige Scans, Risikopriorisierung (z. B. nach CVSS) "
                "und koordinierte Behebung. Tools wie Nessus, OpenVAS oder Qualys unterstützen die "
                "automatisierte Erkennung."
            ),
            "synonyms": ["Vulnerability Management"],
            "sources": [],
        },
    ],
    "Compliance & Recht": [
        {
            "keyword": "DSGVO",
            "definition": "Datenschutz-Grundverordnung – EU-weite Regelung zum Schutz personenbezogener Daten.",
            "description": (
                "Die DSGVO gilt seit Mai 2018 und reguliert die Verarbeitung personenbezogener Daten in der EU. "
                "Wesentliche Prinzipien: Datensparsamkeit, Zweckbindung, Transparenz, Betroffenenrechte "
                "und Meldepflicht bei Datenschutzverletzungen (72 Stunden)."
            ),
            "synonyms": ["GDPR", "Datenschutzgrundverordnung"],
            "sources": [{"name": "DSGVO Volltext", "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679"}],
        },
        {
            "keyword": "ISO/IEC 27001",
            "definition": "Internationale Norm für Informationssicherheits-Managementsysteme (ISMS).",
            "description": (
                "ISO 27001 definiert Anforderungen an ein ISMS und ist die wichtigste internationale "
                "Zertifizierungsnorm für Informationssicherheit. Eine Zertifizierung demonstriert "
                "Kunden und Partnern ein systematisches Sicherheitsniveau."
            ),
            "synonyms": ["ISO 27001", "ISMS-Norm"],
            "sources": [{"name": "ISO/IEC 27001", "url": "https://www.iso.org/standard/27001"}],
        },
        {
            "keyword": "BSI IT-Grundschutz",
            "definition": "Methodik des Bundesamts für Sicherheit in der Informationstechnik zur IT-Absicherung.",
            "description": (
                "Der BSI IT-Grundschutz bietet einen systematischen Ansatz zur Informationssicherheit "
                "mit Kompendium, Profilen und Zertifizierung. Er orientiert sich an ISO 27001 und ist "
                "besonders für deutsche Behörden und Unternehmen relevant."
            ),
            "synonyms": ["Grundschutz", "BSI-Standard"],
            "sources": [{"name": "BSI IT-Grundschutz-Kompendium", "url": "https://www.bsi.bund.de/grundschutz"}],
        },
        {
            "keyword": "NIS2-Richtlinie",
            "definition": "EU-Richtlinie zur Cybersicherheit kritischer und wichtiger Einrichtungen.",
            "description": (
                "NIS2 erweitert den Anwendungsbereich gegenüber NIS1 auf viele Branchen und verschärft "
                "Melde- und Sicherheitspflichten. In Deutschland wird sie durch das NIS2UmsuCG umgesetzt. "
                "Verstöße können mit hohen Bußgeldern geahndet werden."
            ),
            "synonyms": ["NIS2", "Network and Information Security Directive"],
            "sources": [{"name": "NIS2-Richtlinie EU", "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32022L2555"}],
        },
        {
            "keyword": "Datenschutz-Folgenabschätzung",
            "definition": "Pflichtprüfung nach DSGVO bei risikoreichen Datenverarbeitungen.",
            "description": (
                "Eine DSFA (Data Protection Impact Assessment, DPIA) ist vorgeschrieben, wenn eine "
                "Verarbeitung voraussichtlich ein hohes Risiko für Betroffene birgt. Sie analysiert "
                "Risiken und legt Schutzmaßnahmen fest."
            ),
            "synonyms": ["DSFA", "DPIA", "Datenschutzfolgenabschätzung"],
            "sources": [],
        },
        {
            "keyword": "Meldepflicht",
            "definition": "Pflicht zur Meldung von Datenschutzverletzungen oder Sicherheitsvorfällen.",
            "description": (
                "Nach DSGVO müssen Datenschutzverletzungen innerhalb von 72 Stunden der zuständigen "
                "Aufsichtsbehörde gemeldet werden. NIS2 verpflichtet betroffene Einrichtungen zur "
                "gestuften Meldung: Frühwarnung (24h), Erstmeldung (72h), Abschlussbericht (1 Monat)."
            ),
            "synonyms": ["Notifizierungspflicht", "Berichtspflicht"],
            "sources": [],
        },
    ],
}


def run():
    db = SessionLocal()
    try:
        existing = db.query(GlossaryCategory).count()
        if existing > 0:
            print(f"Glossary already seeded ({existing} categories). Skipping.")
            return

        print("Seeding glossary...")
        cat_map: dict[str, GlossaryCategory] = {}

        for cat_data in CATEGORIES:
            cat = GlossaryCategory(
                id=str(uuid.uuid4()),
                name=cat_data["name"],
                description=cat_data["description"],
                image_src=cat_data.get("image_src"),
            )
            db.add(cat)
            cat_map[cat_data["name"]] = cat
        db.flush()

        term_keyword_map: dict[str, GlossaryTerm] = {}

        for cat_name, terms in TERMS.items():
            cat = cat_map[cat_name]
            for t_data in terms:
                term = GlossaryTerm(
                    id=str(uuid.uuid4()),
                    category_id=cat.id,
                    keyword=t_data["keyword"],
                    definition=t_data.get("definition"),
                    description=t_data.get("description"),
                )
                db.add(term)
                db.flush()

                for syn in t_data.get("synonyms", []):
                    db.add(GlossarySynonym(id=str(uuid.uuid4()), term_id=term.id, value=syn))

                for src in t_data.get("sources", []):
                    db.add(GlossarySource(
                        id=str(uuid.uuid4()),
                        term_id=term.id,
                        name=src["name"],
                        url=src["url"],
                    ))

                term_keyword_map[t_data["keyword"]] = term

        CROSS_REFS = [
            ("Informationssicherheit", "CIA-Triade"),
            ("Informationssicherheit", "Risikoanalyse"),
            ("CIA-Triade", "Vertraulichkeit"),
            ("CIA-Triade", "Integrität"),
            ("CIA-Triade", "Verfügbarkeit"),
            ("Ransomware", "Backup"),
            ("Ransomware", "Malware"),
            ("Phishing", "Social Engineering"),
            ("Phishing", "Malware"),
            ("Multi-Faktor-Authentifizierung", "Authentifizierung"),
            ("Penetrationstest", "Schwachstellenmanagement"),
            ("SIEM", "Incident Response"),
            ("Firewall", "Netzwerksegmentierung"),
            ("Zero Trust", "Multi-Faktor-Authentifizierung"),
            ("Zero Trust", "Prinzip der minimalen Rechtevergabe"),
            ("DSGVO", "Datenschutz-Folgenabschätzung"),
            ("DSGVO", "Meldepflicht"),
            ("NIS2-Richtlinie", "Meldepflicht"),
            ("BSI IT-Grundschutz", "Schutzbedarfsfeststellung"),
            ("BSI IT-Grundschutz", "ISO/IEC 27001"),
        ]

        for from_kw, to_kw in CROSS_REFS:
            from_term = term_keyword_map.get(from_kw)
            to_term = term_keyword_map.get(to_kw)
            if from_term and to_term:
                db.add(GlossaryReference(
                    id=str(uuid.uuid4()),
                    term_id=from_term.id,
                    referenced_term_id=to_term.id,
                ))

        db.commit()
        total_terms = sum(len(v) for v in TERMS.values())
        print(f"Done: {len(CATEGORIES)} categories, {total_terms} terms seeded.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
