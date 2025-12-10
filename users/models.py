from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(
        blank=True, null=True, help_text="Tell the world about your stack."
    )
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar/")

    def __str__(self):
        return self.username
