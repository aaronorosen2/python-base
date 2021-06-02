from django.db import models
# Create your models here.


class FaceSwap(models.Model):
    image = models.ImageField(upload_to="media/image",blank=True,null=True)
    video = models.FileField(upload_to="media/video",blank=True,null=True)
    result = models.FileField(blank=True,null=True)

class UploadImage(models.Model):
    upload_image = models.ImageField(upload_to="uploadimg/",blank=True,null=True)