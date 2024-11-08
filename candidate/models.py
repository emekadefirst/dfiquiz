import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


def candidate_id():
    return f"ID{str(uuid.uuid4())[:10]}"


class Candidate(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    other_name = models.CharField(max_length=55, null=True, blank=True)
    full_name = models.CharField(max_length=105, null=True, blank=True)
    candidate_id = models.CharField(max_length=25, null=True, default=candidate_id, unique=True)

    def save(self, *args, **kwargs):
        if self.other_name:
            self.full_name = f"{self.first_name} {self.other_name} {self.last_name}"
        else:
            self.full_name = f"{self.first_name} {self.last_name}"
        super(Candidate, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name or f"{self.first_name} {self.last_name}"
