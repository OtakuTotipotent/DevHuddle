from django.db import models
from django.conf import settings


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username.upper()} - {self.created_at:%Y-%m-%d %H:%M}"
