import os

from django.conf import settings
from django.db import models

IMAGES_FOLDER = os.path.join(settings.MEDIA_ROOT, 'images')


class Image(models.Model):
    file = models.ImageField(upload_to=IMAGES_FOLDER)

    def __str__(self):
        return os.path.basename(self.file.name)
