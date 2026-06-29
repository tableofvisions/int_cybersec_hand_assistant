import logging

import resend

from app.config import settings

logger = logging.getLogger(__name__)


def _send(*, to: str, subject: str, html: str) -> None:
    if not settings.resend_api_key:
        logger.warning("[EMAIL] RESEND_API_KEY not set — skipping send to %s | %s", to, subject)
        return

    try:
        resend.api_key = settings.resend_api_key
        resend.Emails.send({
            "from": settings.resend_from_email,
            "to": [to],
            "subject": subject,
            "html": html,
        })
        logger.info("[EMAIL] Sent '%s' to %s", subject, to)
    except Exception as exc:
        logger.error("[EMAIL] Failed to send '%s' to %s: %s", subject, to, exc)


def send_verification_email(to_email: str, first_name: str, token: str) -> None:
    url = f"{settings.frontend_url}/auth/verify?token={token}"
    _send(
        to=to_email,
        subject="E-Mail-Adresse bestätigen",
        html=f"""
        <p>Hallo {first_name},</p>
        <p>bitte bestätige deine E-Mail-Adresse mit dem folgenden Link:</p>
        <p><a href="{url}">{url}</a></p>
        <p>Der Link ist 24 Stunden gültig.</p>
        """,
    )


def send_password_reset_email(to_email: str, first_name: str, token: str) -> None:
    url = f"{settings.frontend_url}/auth/reset?token={token}"
    _send(
        to=to_email,
        subject="Passwort zurücksetzen",
        html=f"""
        <p>Hallo {first_name},</p>
        <p>du hast eine Anfrage zum Zurücksetzen deines Passworts gestellt.</p>
        <p><a href="{url}">Passwort jetzt zurücksetzen</a></p>
        <p>Der Link ist 2 Stunden gültig. Falls du diese Anfrage nicht gestellt hast, kannst du diese E-Mail ignorieren.</p>
        """,
    )


def send_invite_email(to_email: str, first_name: str, token: str, inviter_name: str) -> None:
    url = f"{settings.frontend_url}/auth/verify?token={token}"
    _send(
        to=to_email,
        subject=f"Einladung von {inviter_name}",
        html=f"""
        <p>Hallo {first_name},</p>
        <p>{inviter_name} hat dich eingeladen, dem Cybersicherheitsassistenten beizutreten.</p>
        <p><a href="{url}">Einladung annehmen und Konto aktivieren</a></p>
        <p>Der Link ist 24 Stunden gültig.</p>
        """,
    )
