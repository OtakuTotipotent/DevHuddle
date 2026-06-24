from .models import Notification, Message


def unread_notifications_count(request):
    if request.user.is_authenticated:
        notif_count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
        dm_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return {
            "unread_count": notif_count,
            "unread_dms_count": dm_count,  # 👈 NEW: Inject into all templates
            "total_alerts": notif_count + dm_count,
        }
    return {"unread_count": 0, "unread_dms_count": 0, "total_alerts": 0}
