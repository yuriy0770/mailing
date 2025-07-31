from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Mailing, MailingAttempt

def send_mailing_emails(mailing):
    mailing.status = 'started'
    if not mailing.first_send:
        mailing.first_send = now()
    mailing.save()

    clients = mailing.clients.all()

    for client in clients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email='no-reply@example.com',
                recipient_list=[client.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                status='success',
                server_response='Отправлено успешно',
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                status='failed',
                server_response=str(e),
            )
    mailing.finish_send = now()
    mailing.status = 'finished'
    mailing.save()