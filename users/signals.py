# /users/signals.py

import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from feed.models import Notification
from .models import CustomUser


@receiver(post_delete, sender=CustomUser)
def delete_avatar_on_account_delete(sender, instance, **kwargs):
    if instance.avatar and instance.avatar.name != "avatars/default.png":
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(pre_save, sender=CustomUser)
def delete_old_avatar_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_avatar = CustomUser.objects.get(pk=instance.pk).avatar
    except CustomUser.DoesNotExist:
        return False

    new_avatar = instance.avatar
    if (
        old_avatar
        and old_avatar != new_avatar
        and old_avatar.name != "avatars/default.png"
    ):
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)


@receiver(post_save, sender=CustomUser)
def create_welcome_notification(sender, instance, created, **kwargs):
    # Only run when user is FIRST created.
    if created:
        Notification.objects.create(
            recipient=instance,
            actor=instance,
            verb="welcome",
            is_read=False,
        )


@receiver(user_logged_in)
def cancel_account_deletion(sender, user, request, **kwargs):
    """Intercepts a login. If the user was scheduled for deletion, cancel it."""
    if user.deletion_scheduled_at:
        user.deletion_scheduled_at = None
        user.save()

        # Alert them on the screen
        messages.success(
            request,
            "Welcome back! Your account deletion request has been successfully cancelled.",
        )

        # Send an internal system notification
        Notification.objects.create(recipient=user, actor=user, verb="alert")
