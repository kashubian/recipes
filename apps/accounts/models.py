from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username