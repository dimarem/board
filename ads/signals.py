from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Feedback


@receiver(post_save, sender=Feedback)
def send_feedback_notification(sender, instance, created, **kwargs):
    """Отправить письмо об уведомлении автору объявления"""
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

        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(pre_save, sender=Feedback)
def send_feedback_acceptance(sender, instance, **kwargs):
    """Отправить письмо о принятии автору отзыва"""
    if instance.accepted:
        prev = Feedback.objects.get(pk=instance.id)

        if not prev.accepted and instance.accepted:
            html_content = render_to_string('feedback_accepted.html', {
                'feedback': instance
            })

            msg = EmailMultiAlternatives(
                subject='Отзыв принят',
                body='',
                from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
                to=[instance.author.email]
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

