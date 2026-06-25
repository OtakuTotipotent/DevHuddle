from django.db import models
from django.conf import settings
from feed.models import Post

# ==========================================
# STORE THE GENERATED AI REPORTS
# ==========================================


class AIReport(models.Model):
    REPORT_TYPES = (
        ("profile", "Profile Analysis"),
        ("post", "Post Review"),
    )
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="requested_ai_reports",
    )

    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ai_profile_reports",
    )

    target_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True
    )

    # The AI Data
    content = models.TextField(help_text="Markdown formatted AI response")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.get_report_type_display()} requested by {self.requester.username}"
        )
