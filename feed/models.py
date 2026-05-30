import os
import uuid
from django.utils.timezone import now
from django.db import models
from django.conf import settings
from users.validators import validate_file_size, validate_image_extension
from users.models import CustomUser


def rename_post_image(instance, filename):
    extension = filename.split(".")[-1]
    filename = f"{instance.author.username}_{now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{extension}"  # Format: username_YYYYMMDD_HHMMSS_uuid.jpg

    return os.path.join("post", filename)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)

    image = models.ImageField(
        upload_to=rename_post_image,
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_extension],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    POST_TYPES = (
        ("huddle", "Huddle"),  # Standard social post
        ("job", "Job/Offer"),  # Business feed
        ("ad", "Advertisement"),  # Advertiser feed
    )
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default="huddle")
    is_boosted = models.BooleanField(default=False)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True
    )

    deadline = models.DateTimeField(
        null=True, blank=True, help_text="For Ads/Jobs only"
    )
    target_url = models.URLField(
        null=True, blank=True, help_text="Link for the Ad button"
    )
    tags = models.CharField(
        max_length=100,
        blank=True,
        help_text="Comma separated tags (e.g. #python, #remote)",
    )

    def __str__(self):
        return f"{self.author.username.upper()} - {self.created_at:%Y-%m-%d %H:%M}"

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

    @property
    def is_parent(self):
        """Helper to easily filter top-level comments in templates."""
        return self.parent is None


class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="triggered_notifications"
    )

    VERB_CHOICES = (
        ("welcome", "Welcome! You can now update your profile in settings"),
        ("premium", "Upgrade to Premium to unlock exclusive developer tools!"),
        ("like", "liked your post"),
        ("comment", "commented on your post"),
        ("reply", "replied to your comment"),
        ("follow", "started following you"),
        ("block", "has blocked you"),
        ("boost", "boosted you"),
        ("connect", "sent you a connection request"),
        ("dm", "sent you a direct message (DM)"),
        ("hire", "wants to hire you"),
        ("profile", "checked your profile"),
        ("visit", "visited your profile"),
    )
    verb = models.CharField(max_length=26, choices=VERB_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def theme(self):
        """Returns Tailwind classes based on the verb."""
        themes = {
            "welcome": {
                "border": "border-purple-500/50",
                "text": "text-purple-500",
                "bg": "bg-purple-500/10",
            },
            "premium": {
                "border": "border-yellow-500/50",
                "text": "text-yellow-500",
                "bg": "bg-yellow-500/10",
            },
            "block": {
                "border": "border-red-500/50",
                "text": "text-red-500",
                "bg": "bg-red-500/10",
            },
            "hire": {
                "border": "border-green-500/50",
                "text": "text-green-500",
                "bg": "bg-green-500/10",
            },
            "profile": {
                "border": "border-white/50",
                "text": "text-white/50",
                "bg": "bg-white/50",
            },
            "default": {
                "border": "border-blue-500/50",
                "text": "text-blue-500",
                "bg": "bg-blue-500/10",
            },
        }
        return themes.get(self.verb, themes["default"])
