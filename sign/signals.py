import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import ConfirmationCode


@receiver(post_save, sender=User)
def send_email_confirmation_link(sender, instance, created, **kwargs):
    """Отправить письмо с кодом подтверждения"""
    if created:
        confirmation_code = ConfirmationCode.objects.create(user=instance, code=random.randint(10000, 100000))

        html_content = render_to_string('email_confirmation.html', {
            'user': instance,
            'confirmation_code': confirmation_code
        })

        msg = EmailMultiAlternatives(
            subject=f'Добро пожаловать {instance.username}',
            body='',
            from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
            to=[instance.email]
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
