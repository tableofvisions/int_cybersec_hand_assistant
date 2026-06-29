"""Seed incident data from the original frontend hardcoded values."""
import uuid

from app.database import SessionLocal
from app.models.incidents import (
    EmergencyContact,
    IncidentLink,
    IncidentLinkCategory,
    IncidentSign,
    IncidentSignExample,
)

_CONTACTS = [
    {
        "name": "Notfall-Hotline Cyberwehr",
        "phone": "0800-CYBERWEHR",
        "bh_always": True,
    },
    {
        "name": "Service Center des BSI",
        "phone": "0800 274 1000",
        "bh_always": False,
        "bh_weekday_start": 1,
        "bh_weekday_end": 5,
        "bh_time_start": 480,   # 08:00
        "bh_time_end": 1080,    # 18:00
    },
    {
        "name": "Ansprechstellen Cybercrime Baden-Württemberg",
        "phone": "0711 5401 2444",
        "bh_always": True,
    },
    {
        "name": "Ansprechstellen Cybercrime Bundeskriminalamt",
        "phone": "0611 55 15037",
        "bh_always": True,
    },
]

_SIGNS = [
    {
        "title": "Ungewöhnliches Systemverhalten",
        "description": (
            "Systeme oder Geräte verhalten sich anders als üblich, z. B. unerwartete Abstürze, "
            "hohe Prozessorlast oder unbekannte Programme."
        ),
        "examples": [
            "Ein PC wird extrem langsam, obwohl keine ressourcenintensiven Programme laufen.",
            "Plötzlich auftretende Pop-ups oder Warnmeldungen, die zuvor nicht da waren.",
            "Software, die ohne Nutzeraktion installiert wurde.",
        ],
    },
    {
        "title": "Ungewöhnliche E-Mail-Kommunikation",
        "description": (
            "E-Mails, die unerwartet oder verdächtig erscheinen, wie z. B. Phishing-Versuche, "
            "gefälschte Absenderadressen oder E-Mails mit schädlichen Anhängen."
        ),
        "examples": [
            "E-Mails von vermeintlichen Partnern, die ungewöhnliche Zahlungsanweisungen oder -forderungen enthalten.",
            "E-Mails mit Anhängen im .zip- oder .exe-Format, die ohne Kontext gesendet werden.",
            "Aufforderungen, Zugangsdaten einzugeben, die auf externe Websites führen.",
        ],
    },
    {
        "title": "Ungewöhnliche Telefonanrufe",
        "description": (
            "Telefonanrufe von unbekannten Personen, die versuchen, sensible Informationen zu erhalten "
            "oder Druck ausüben, um Handlungen wie Zahlungen durchzuführen."
        ),
        "examples": [
            "Anrufe von angeblichen IT-Support-Diensten, die Zugang zu Systemen fordern.",
            "Drohanrufe, die Zahlungen oder Informationen verlangen.",
            "Rückrufaufforderungen an verdächtige Telefonnummern.",
        ],
    },
    {
        "title": "Antivirus- und Sicherheitswarnungen",
        "description": (
            "Warnmeldungen von Sicherheitssoftware, die auf Bedrohungen hinweisen, "
            "wie Malware, Ransomware oder verdächtige Aktivitäten."
        ),
        "examples": [
            "Die Sicherheitssoftware meldet wiederholt das gleiche infizierte Programm.",
            "Ein plötzlicher Ausfall oder die Deaktivierung von Antivirensoftware.",
            "Hinweise auf blockierte Verbindungen zu Command-and-Control-Servern.",
        ],
    },
    {
        "title": "Unerwartete Benutzerkontenaktivitäten",
        "description": (
            "Aktivitäten, die nicht zu den üblichen Benutzergewohnheiten passen, wie z. B. "
            "Anmeldungen außerhalb der normalen Arbeitszeiten oder von ungewöhnlichen Orten."
        ),
        "examples": [
            "Ein Benutzerkonto meldet sich um 3 Uhr morgens an, obwohl der Mitarbeiter nur tagsüber arbeitet.",
            "Anmeldungen von unbekannten IP-Adressen oder Ländern, in denen das Unternehmen nicht tätig ist.",
            "Zugriffe auf Dateien oder Systeme, auf die der Benutzer normalerweise keinen Zugriff benötigt.",
        ],
    },
    {
        "title": "Mitarbeitermeldungen",
        "description": "Mitarbeiter berichten von verdächtigen Beobachtungen oder ungewöhnlichen Aktivitäten in IT-Systemen.",
        "examples": [
            "Ein Mitarbeiter meldet, dass seine Passwörter plötzlich nicht mehr funktionieren.",
            "Ein Benutzer berichtet, dass er Dateien nicht mehr öffnen kann, die er vorher regelmäßig verwendet hat.",
            "Verdächtige Änderungen an persönlichen oder geschäftlichen Konten, z. B. geänderte Bankverbindungen.",
        ],
    },
    {
        "title": "Ungewöhnliche Dateiänderungen",
        "description": (
            "Dateien oder Konfigurationen werden ohne legitimen Grund geändert oder gelöscht. "
            "Dies kann ein Hinweis auf Ransomware oder Malware sein."
        ),
        "examples": [
            "Plötzliche Verschlüsselung von Dateien mit ungewöhnlichen Dateiendungen (z. B. .crypt oder .locked).",
            "Änderungen an wichtigen Konfigurationsdateien, die zu Systemproblemen führen.",
            "Veränderte Prüf-Hashes (MD5, SHA256) bei Dateien, die eigentlich unverändert bleiben sollten.",
        ],
    },
    {
        "title": "Netzwerkanomalien",
        "description": (
            "Unerklärliche oder ungewöhnliche Aktivitäten im Netzwerkverkehr, wie Datenübertragungen "
            "zu unbekannten Servern oder unerwartete Verbindungsversuche."
        ),
        "examples": [
            "Ein stark erhöhtes Datenaufkommen zu unbekannten IP-Adressen, insbesondere ins Ausland.",
            "Netzwerkgeräte, die auf Ports kommunizieren, die normalerweise nicht genutzt werden.",
            "Unbekannte Geräte im lokalen Netzwerk.",
        ],
    },
]

_LINK_CATEGORIES = [
    {
        "title": "Externe Unterstützung",
        "links": [
            {"title": "Industrie- und Handelskammer", "url": "https://www.ihk.de/daten-und-informationssicherheit"},
            {
                "title": "[ZDH] IT-Sicherheitsbotschafter Ihrer Handwerkskammer",
                "url": "https://cybersicherheit-handwerk.de/Sicherheitsbotschafter",
            },
            {
                "title": "[ZDH] Fachberater IT-Sicherheit",
                "url": "https://cybersicherheit-handwerk.de/cgi-bin/scgi?sid=1&se=1&kd=0&sp=deu&rid=179&bef=neueseite",
            },
            {
                "title": "[ZDH] IT-Grundschutz-Praktiker",
                "url": "https://cybersicherheit-handwerk.de/cgi-bin/scgi?sid=1&se=1&kd=0&sp=deu&rid=180&bef=neueseite",
            },
            {
                "title": "[BSI] Liste zertifizierter IT-Sicherheitsdienstleister (IS-Revision und IS-Penetrationstests)",
                "url": (
                    "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/"
                    "Zertifizierung-und-Anerkennung/Anerkennung-von-Stellen-und-Zertifizierung-IT-Sicherheits"
                    "dienstleister/IS-Rev/is-rev_node.html"
                ),
            },
            {
                "title": "[BSI] Liste der qualifizierten APT-Response-Dienstleister",
                "url": (
                    "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Cyber-Sicherheit/Themen/"
                    "Dienstleister_APT-Response-Liste.pdf?__blob=publicationFile&v=34"
                ),
            },
            {
                "title": "[BSI] Liste qualifizierter DDoS-Mitigation-Dienstleister",
                "url": (
                    "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Cyber-Sicherheit/Themen/"
                    "Dienstleister-DDos-Mitigation-Liste.pdf?__blob=publicationFile&v=18"
                ),
            },
            {
                "title": "[BSI] Liste IT-Sicherheitsdienstleister im Bereich Lauschabwehr",
                "url": (
                    "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/"
                    "Zertifizierung-und-Anerkennung/Anerkennung-von-Stellen-und-Zertifizierung-IT-Sicherheits"
                    "dienstleister/Lauschabwehr-im-Bereich-der-Wirtschaft/Liste-IT-Sicherheitsdienstleister/"
                    "liste-it-sicherheitsdienstleister_node.html"
                ),
            },
        ],
    },
    {
        "title": "Hilfe zur Selbsthilfe (BSI)",
        "links": [
            {
                "title": "TOP 12 Maßnahmen bei Cyber-Angriffen",
                "url": (
                    "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-"
                    "Empfehlungen/Empfehlungen-nach-Angriffszielen/Unternehmen-allgemein/IT-Notfallkarte/"
                    "TOP-12-Massnahmen/top-12-massnahmen_node.html"
                ),
            },
            {
                "title": "Maßnahmenkatalog zum Notfallmanagement – Fokus IT-Notfälle",
                "url": (
                    "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-"
                    "Empfehlungen/Empfehlungen-nach-Angriffszielen/Unternehmen-allgemein/IT-Notfallkarte/"
                    "Massnahmenkatalog/massnahmenkatalog_node.html"
                ),
            },
            {
                "title": "Erste Hilfe bei einem schweren IT-Sicherheitsvorfall Version 1.1",
                "url": (
                    "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Cyber-Sicherheit/Themen/"
                    "Ransomware_Erste-Hilfe-IT-Sicherheitsvorfall.html?nn=133632#download=1"
                ),
            },
        ],
    },
    {
        "title": "Sicherheitswarnungen und Schwachstellen",
        "links": [
            {
                "title": "[BSI] Cyber-Sicherheitswarnungen",
                "url": (
                    "https://www.bsi.bund.de/SiteGlobals/Forms/Suche/BSI/Sicherheitswarnungen/"
                    "Sicherheitswarnungen_Formular.html?nn=133020&cl2Categories_DocType=callforbids"
                ),
            },
            {
                "title": "[CERT-Bund] Sicherheitswarnungen",
                "url": "https://wid.cert-bund.de/portal/wid/kurzinformationen",
            },
        ],
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(EmergencyContact).count() > 0:
            print("Incident seed data already present – skipping.")
            return

        for i, c in enumerate(_CONTACTS):
            db.add(EmergencyContact(
                id=str(uuid.uuid4()),
                sort_order=i,
                name=c["name"],
                phone=c.get("phone"),
                mail=c.get("mail"),
                url=c.get("url"),
                bh_always=c.get("bh_always", False),
                bh_weekday_start=c.get("bh_weekday_start"),
                bh_weekday_end=c.get("bh_weekday_end"),
                bh_time_start=c.get("bh_time_start"),
                bh_time_end=c.get("bh_time_end"),
            ))

        for i, s in enumerate(_SIGNS):
            sign_id = str(uuid.uuid4())
            db.add(IncidentSign(id=sign_id, sort_order=i, title=s["title"], description=s["description"]))
            for j, ex in enumerate(s["examples"]):
                db.add(IncidentSignExample(id=str(uuid.uuid4()), sign_id=sign_id, sort_order=j, text=ex))

        for i, cat in enumerate(_LINK_CATEGORIES):
            cat_id = str(uuid.uuid4())
            db.add(IncidentLinkCategory(id=cat_id, sort_order=i, title=cat["title"]))
            for j, lnk in enumerate(cat["links"]):
                db.add(IncidentLink(id=str(uuid.uuid4()), category_id=cat_id, sort_order=j, title=lnk["title"], url=lnk["url"]))

        db.commit()
        print("Incident seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
