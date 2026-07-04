from django.db.models import Count, Case, When, IntegerField, ExpressionWrapper, F
from django.utils.timezone import now
from .models import Notification, Message
from users.models import CustomUser


def unread_notifications_count(request):
    context = {
        "unread_count": 0,
        "unread_dms_count": 0,
        "total_alerts": 0,
        "user_rank": "N/A",
    }

    if request.user.is_authenticated:
        notif_count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
        dm_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        context.update(
            {
                "unread_count": notif_count,
                "unread_dms_count": dm_count,
                "total_alerts": notif_count + dm_count,
            }
        )

        # Calculate Global Rank for the Dropdown
        if request.user.role == "dev":
            ranked_devs = (
                CustomUser.objects.filter(role="dev")
                .annotate(
                    follower_count=Count("followers", distinct=True),
                    project_count=Count("projects", distinct=True),
                    premium_bonus=Case(
                        When(premium_expires_at__gt=now(), then=50),
                        default=0,
                        output_field=IntegerField(),
                    ),
                )
                .annotate(
                    dev_score=ExpressionWrapper(
                        (F("follower_count") * 2)
                        + (F("project_count") * 3)
                        + (F("profile_boosts") * 7)
                        + F("premium_bonus"),
                        output_field=IntegerField(),
                    )
                )
                .order_by("-dev_score", "-date_joined")
            )

            # Execute list index safely
            dev_list = list(ranked_devs.values_list("id", flat=True))
            try:
                context["user_rank"] = f"{dev_list.index(request.user.id) + 1}"
            except ValueError:
                context["user_rank"] = "N/A"
        else:
            context["user_rank"] = "ORG"

    return context
