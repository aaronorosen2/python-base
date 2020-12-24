from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_url = 'http://localhost:8001' + "{}?token={}".format(reverse('courses:password_reset:reset-password-request'),
                                                               reset_password_token.key)

    email_plaintext_message = f'''To reset your password, visit the following link: 

{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Website title"),
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [reset_password_token.user.email]
    )
