from django.db import models
from django.conf import settings
from users.validators import validate_file_size, validate_image_extension


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_extension],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True
    )

    def __str__(self):
        return f"{self.author.username.upper()} - {self.created_at:%Y-%m-%d %H:%M}"

    def total_likes(self):
        return self.likes.count()
