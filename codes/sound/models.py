import uuid
from django.db import models
import os


def uuid_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)


class SoundFile(models.Model):
    file = models.FileField(upload_to=uuid_file_path,
                            blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self) -> str:
        return f"-{self.id} {self.name}-"
