from django.db import models
import uuid


# Author= Muhammad Hammad
# Models for room information and room visitors
class ParentModel(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class RoomInfo(ParentModel):
    room_name = models.CharField(max_length=50, unique=True)
    logo_url = models.TextField()

class RoomVisitors(ParentModel):
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    room = models.ForeignKey(RoomInfo, on_delete=models.CASCADE)

class RoomRecording(ParentModel):
    recording_link = models.TextField()
    room = models.ForeignKey(RoomInfo, on_delete=models.CASCADE)

class Brand(models.Model):
    logo_img_url = models.CharField(max_length=500)
    room_name = models.CharField(max_length=500)


class Vistor(models.Model):
    name = models.CharField(max_length=2000, default='')
    email = models.EmailField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
