from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser
from .validators import validate_image_extension, validate_file_size


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(
        blank=True, null=True, help_text="Tell the world about your stack."
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to="avatar/",
        default="avatars/default.png",
        validators=[validate_file_size, validate_image_extension],
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
