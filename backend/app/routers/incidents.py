from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.auth.deps import get_verified_user
from app.database import get_db
from app.models.incidents import EmergencyContact, IncidentLinkCategory, IncidentSign
from app.models.user import User
from app.schemas.incidents import (
    BusinessHoursOut,
    EmergencyContactOut,
    IncidentLinkCategoryOut,
    IncidentLinkOut,
    IncidentSignOut,
    IncidentStepOut,
)

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

Db = Annotated[Session, Depends(get_db)]
Auth = Annotated[User, Depends(get_verified_user)]

_RESPONSE_STEPS: list[IncidentStepOut] = [
    IncidentStepOut(
        pos=1,
        title="Bewahren Sie Ruhe!",
        text="Handeln Sie nicht übereilt und überlegen Sie sich in Ruhe, wie Sie vorgehen wollen.",
    ),
    IncidentStepOut(
        pos=2,
        title="Keine Passwörter eingeben",
        text=(
            "Keinesfalls darf eine Anmeldung mit privilegierten Nutzerkonten (Administratorkonten) "
            "auf einem potenziell infizierten System erfolgen."
        ),
    ),
    IncidentStepOut(
        pos=3,
        title="Netzwerkkabel ziehen",
        text=(
            "Potenziell infizierte Systeme sollten umgehend von Ihrem Netzwerk getrennt werden, "
            "um ggf. eine weitere Ausbreitung von Schadsoftware auf andere Systeme zu verhindern. "
            "Dazu ziehen Sie das Netzwerkkabel und trennen bestehende WLAN-Verbindungen. "
            "Das System sollte nicht heruntergefahren oder ausgeschaltet werden."
        ),
    ),
    IncidentStepOut(
        pos=4,
        title="Beweise sichern",
        text=(
            "Versuchen Sie das Geschehen bestmöglich zu dokumentieren (z. B. Notizen, Bilder, Videos). "
            "Falls möglich, führen Sie eine Sicherung des Systems inkl. Speicherabbild für spätere Analysen durch."
        ),
    ),
    IncidentStepOut(
        pos=5,
        title="Passwörter ändern",
        text=(
            "Alle auf betroffenen Systemen gespeicherten bzw. nach der Infektion eingegebenen Zugangsdaten "
            "sollten als kompromittiert betrachtet und die Passwörter geändert werden."
        ),
    ),
    IncidentStepOut(
        pos=6,
        title="Externe Unterstützung holen",
        text="Holen Sie sich bei Bedarf frühzeitig externe Unterstützung.",
        sourceLabel="BSI – Digitaler Ersthelfer",
        sourceUrl=(
            "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/"
            "Informationen-und-Empfehlungen/Cyber-Sicherheitsnetzwerk/Qualifizierung/"
            "Digitaler_Ersthelfer/Suche-Ersthelfer/suche-ersthelfer-node.html"
        ),
    ),
    IncidentStepOut(
        pos=7,
        title="Meldepflichten beachten",
        text=(
            "Falls Sie einer gesonderten Meldepflicht unterliegen (z. B. als Teil einer kritischen "
            "Infrastruktur), müssen Sie den Vorfall auf dem dafür vorgeschriebenen Weg melden."
        ),
        sourceLabel="BSI – Meldepflichtige Unternehmen",
        sourceUrl=(
            "https://www.bsi.bund.de/DE/IT-Sicherheitsvorfall/Kritische-Infrastrukturen-und-"
            "meldepflichtige-Unternehmen/kritische-infrastrukturen-und-meldepflichtige-unternehmen"
            ".html?nn=133608&pos=2"
        ),
    ),
    IncidentStepOut(
        pos=8,
        title="Systeme neu aufsetzen",
        text=(
            "Angegriffene Systeme sollten grundsätzlich als vollständig kompromittiert betrachtet werden. "
            "Sie sollten daher vor der erneuten Verwendung des Systems dieses komplett neu aufsetzen oder austauschen."
        ),
        sourceLabel="BSI – Erste Hilfe IT-Sicherheitsvorfall",
        sourceUrl=(
            "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Cyber-Sicherheit/Themen/"
            "Ransomware_Erste-Hilfe-IT-Sicherheitsvorfall.pdf?__blob=publicationFile&v=3"
        ),
    ),
]


@router.get("/emergency-contacts", response_model=list[EmergencyContactOut])
def list_emergency_contacts(db: Db, current_user: Auth):
    contacts = db.query(EmergencyContact).order_by(EmergencyContact.sort_order).all()
    return [
        EmergencyContactOut(
            id=c.id,
            name=c.name,
            phone=c.phone,
            mail=c.mail,
            url=c.url,
            businessHours=BusinessHoursOut(
                always=c.bh_always,
                weekDayStart=c.bh_weekday_start,
                weekDayEnd=c.bh_weekday_end,
                timeStart=c.bh_time_start,
                timeEnd=c.bh_time_end,
            ),
        )
        for c in contacts
    ]


@router.get("/signs", response_model=list[IncidentSignOut])
def list_incident_signs(db: Db, current_user: Auth):
    signs = (
        db.query(IncidentSign)
        .options(joinedload(IncidentSign.examples))
        .order_by(IncidentSign.sort_order)
        .all()
    )
    return [
        IncidentSignOut(
            id=s.id,
            title=s.title,
            description=s.description,
            examples=[e.text for e in s.examples],
        )
        for s in signs
    ]


@router.get("/steps", response_model=list[IncidentStepOut])
def list_response_steps(current_user: Auth):
    return _RESPONSE_STEPS


@router.get("/links", response_model=list[IncidentLinkCategoryOut])
def list_link_categories(db: Db, current_user: Auth):
    categories = (
        db.query(IncidentLinkCategory)
        .options(joinedload(IncidentLinkCategory.links))
        .order_by(IncidentLinkCategory.sort_order)
        .all()
    )
    return [
        IncidentLinkCategoryOut(
            id=c.id,
            title=c.title,
            links=[IncidentLinkOut(title=lnk.title, url=lnk.url) for lnk in c.links],
        )
        for c in categories
    ]
