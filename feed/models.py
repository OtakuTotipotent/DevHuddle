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

    def __str__(self):
        return f"{self.author.username.upper()} - {self.created_at:%Y-%m-%d %H:%M}"

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="triggered_notifications"
    )

    VERB_CHOICES = (
        ("like", "liked your post"),
        ("comment", "commented on your post"),
        ("follow", "started following you"),
        ("block", "blocked you"),
        ("boost", "boosted you"),
        ("connect", "sent you a connection"),
        ("dm", "sent you a message"),
        ("hire", "wants to hire you"),
        ("profile", "checked your profile"),
        ("visit", "visited your profile"),
    )
    verb = models.CharField(max_length=26, choices=VERB_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
