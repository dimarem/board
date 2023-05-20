from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Feedback


@receiver(post_save, sender=Feedback)
def send_feedback_notification(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string('feedback_notification.html', {
            'feedback': instance
        })

        msg = EmailMultiAlternatives(
            subject=f'Отзыв на объявление {instance.ad.preview}',
            body='',
            from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
            to=[instance.ad.author.user.email]
        )

        print(instance.ad.author)

        msg.attach_alternative(html_content, "text/html")
        msg.send()

