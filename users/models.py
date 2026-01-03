import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image, ImageOps
from .validators import validate_image_extension, validate_file_size


def rename_avatar(instance, filename):
    extension = filename.split(".")[-1]
    filename = f"{instance.username}.{extension}"
    return os.path.join("avatar", filename)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(
        blank=True, null=True, help_text="Tell the world about your stack."
    )

    # URL Fields
    github_url = models.URLField(
        blank=True, null=True, help_text="Link to your github profile"
    )
    linkedin_url = models.URLField(
        blank=True, null=True, help_text="Link to your linkedin profile"
    )
    twitter_url = models.URLField(
        blank=True, null=True, help_text="Link to your X (formerly twitter) profile"
    )
    stackoverflow_url = models.URLField(
        blank=True, null=True, help_text="Link to your StackOverflow profile"
    )
    portfolio_url = models.URLField(
        blank=True, null=True, help_text="Your Portfolio website link"
    )
    fiver_url = models.URLField(
        blank=True, null=True, help_text="Your Fiver profile link"
    )
    upwork_url = models.URLField(
        blank=True, null=True, help_text="Your Upwork profile link"
    )

    # Social Fields
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to=rename_avatar,
        validators=[validate_file_size, validate_image_extension],
    )

    def is_following(self, target_user):
        return self.following.filter(pk=target_user.pk).exists()

    def is_followed_by(self, target_user):
        return self.followers.filter(pk=target_user.pk).exists()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img = ImageOps.fit(img, output_size, centering=(0.5, 0.5))
                    img.save(self.avatar.path)
            except Exception as e:
                print(f"Image processing failed: {e}")
