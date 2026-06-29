import os
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Notification, Post


@receiver(post_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Post)
def delete_old_post_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = Post.objects.get(pk=instance.pk).image
    except Post.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


# Websocket & Communications
@receiver(post_save, sender=Notification)
def broadcast_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f"notifications_{instance.recipient.id}"

        # Prepare the payload
        payload = {
            "type": "send_notification",
            "verb": instance.get_verb_display(),
            "actor": instance.actor.username,
            "icon": instance.icon or "🔔",
        }

        # Send over WebSockets
        async_to_sync(channel_layer.group_send)(group_name, payload)
