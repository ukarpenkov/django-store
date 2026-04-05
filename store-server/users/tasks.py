import logging

from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_verification_email_task(
    subject: str,
    message: str,
    from_email: str,
    recipient_list: list[str],
) -> None:
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except Exception as exc:
        logger.exception(
            "Не удалось отправить письмо верификации на %s: %s",
            recipient_list,
            exc,
        )
