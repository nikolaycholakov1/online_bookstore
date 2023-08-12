from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from online_bookstore import settings
from online_bookstore.apps.book.models import Customer


def send_success_register_email(user):
    html_message = render_to_string(
        'email/registration-greeting.html',
        {'user': user},
    )

    plain_message = strip_tags(html_message)

    send_mail(
        subject='Registration greetings',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(user.email,)
    )


@receiver(post_save, sender=Customer)
def user_created(instance, created, **kwargs):
    if created:
        send_success_register_email(instance)
