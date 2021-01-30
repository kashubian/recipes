from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def set_username(self):
        if self.username == "":
            self.username = self.email.split("@")[0]

    def save(self, *args, **kwargs):
        self.set_username()
        super(CustomUser, self).save(*args, **kwargs)

