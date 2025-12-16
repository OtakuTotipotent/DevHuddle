import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
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
