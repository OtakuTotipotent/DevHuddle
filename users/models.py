# /users/models.py

import os
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser

from config import settings
from .validators import validate_image_extension, validate_file_size, validate_username


def rename_avatar(instance, filename):
    extension = filename.split(".")[-1]
    filename = f"{instance.username}.{extension}"
    return os.path.join("avatar", filename)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(3), validate_username],
        error_messages={
            "unique": "A user with same username already exists.",
            "min_length": "Username must be at least 4 characters long.",
        },
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(
        blank=True, null=True, help_text="Tell the world about your stack."
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to=rename_avatar,
        validators=[validate_file_size, validate_image_extension],
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

    # Role
    ROLE_CHOICES = (
        ("dev", "Developer"),
        ("client", "Client / Hirer"),
        ("org", "Organization"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="dev")
    tech_stack = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g. Python, Java, CI/CD, Unity... (Comma separated)",
    )

    # Monetization | Pricing
    premium_expires_at = models.DateTimeField(
        blank=True, null=True, help_text="When the Pro subscription ends"
    )
    profile_boosts = models.IntegerField(
        default=0,
        help_text="Number of profile boosts purchased",
    )

    # methods & properties
    @property
    def is_premium(self):
        """Dynamically calculates premium status without needing background cron jobs"""
        if self.premium_expires_at:
            return self.premium_expires_at > now()
        return False

    def is_following(self, target_user):
        return self.following.filter(pk=target_user.pk).exists()

    def is_followed_by(self, target_user):
        return self.followers.filter(pk=target_user.pk).exists()

    def __str__(self):
        return self.username


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="skills", blank=True
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    live_url = models.URLField(
        blank=True, null=True, help_text="Link to the live project"
    )
    github_url = models.URLField(
        blank=True, null=True, help_text="Link to the source code"
    )
    # Optional thumbnail
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_extension],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class Experience(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="experiences"
    )
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    start_date = models.DateField()
    end_date = models.DateField(
        blank=True, null=True, help_text="Leave blank if currently working here"
    )
    is_current = models.BooleanField(default=False)

    description = models.TextField(max_length=1000, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.role} at {self.company}"
