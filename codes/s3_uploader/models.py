from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
import uuid
import os
from django.db import models

# # Author= Muhammad Hammad
# # Models for room information and room visitors
# class ParentModel(models.Model):
#     id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

# class RoomInfo(ParentModel):
#     room_name = models.CharField(max_length=50, unique=True)
#     logo_url = models.TextField()

# class RoomVisitors(ParentModel):
#     user_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=20)
#     room = models.ForeignKey(RoomInfo, on_delete=models.CASCADE)

# class RoomRecording(ParentModel):
#     recording_link = models.TextField()
#     room = models.ForeignKey(RoomInfo, on_delete=models.CASCADE)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Link to password reset page
    SERVER_URL = "https://sfapp.dreamstate-4-all.org"
    # SERVER_URL = "http://localhost:8084"

    reset_url = "{}/cardone.html?token={}".format(SERVER_URL, reset_password_token.key)


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
