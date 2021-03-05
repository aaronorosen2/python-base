from django.db import models
import uuid
from datetime import datetime    


# Author= Muhammad Hammad
# Models for room information and room visitors
class ParentModel(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True

class RoomInfo(ParentModel):
    room_name = models.CharField(max_length=50, unique=True)
    logo_url = models.TextField()
    video_url = models.CharField(max_length=500,default='')
    slack_channel = models.CharField(max_length=500, unique=True)

    class Meta:
        db_table = "roominfo"

class RoomVisitors(ParentModel):
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    room = models.ForeignKey(RoomInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = "roomvisitors"

class RoomRecording(ParentModel):
    recording_link = models.TextField()
    room = models.ForeignKey(RoomInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = "roomrecording"

class Brand(ParentModel):
    logo_url = models.CharField(max_length=500)
    room_name = models.CharField(max_length=500, unique=True)
    video_url = models.CharField(max_length=500,default='')
    slack_channel = models.CharField(max_length=500)


class Visitor(ParentModel):
    user_name = models.CharField(max_length=2000, default='')
    email = models.EmailField(max_length=512, blank=True, null=True)
    phone_number = models.CharField(max_length=24, blank=True, null=True)
    room = models.ForeignKey(Brand, on_delete=models.CASCADE)

class Recording(ParentModel):
    recording_link = models.TextField()
    room = models.ForeignKey(Brand, on_delete=models.CASCADE)

class Categories(ParentModel):
    category = models.CharField(max_length=100)
    description = models.TextField()

# class CategoriesVisitor(ParentModel):

