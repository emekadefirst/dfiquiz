import uuid
from io import BytesIO
from django.db import models
from server.cloud import cloud
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class Examiner(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload = models.ImageField(upload_to="images") 
    organization_name = models.CharField(max_length=55, null=True, blank=True, unique=True)
    url = models.URLField(max_length=200, null=True, blank=True) 
    image = models.URLField(max_length=1000, null=True, blank=True)
    address = models.TextField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        if self.upload and not self.image_url:
            sanitized_name = slugify(self.upload.name)
            image_data = BytesIO(self.upload.read())
            self.image_url = cloud(image_data, sanitized_name) 
            self.upload.delete(save=False) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.organization_name
