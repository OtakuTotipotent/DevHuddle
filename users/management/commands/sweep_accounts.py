from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser


class Command(BaseCommand):
    help = "Sweeps the database and permanently deletes accounts past their 3-day grace period."

    def handle(self, *args, **kwargs):
        # Find users where deletion_scheduled_at is NOT null, AND the time has passed
        expired_users = CustomUser.objects.filter(
            deletion_scheduled_at__isnull=False, deletion_scheduled_at__lte=now()
        )

        count = expired_users.count()
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS("No accounts scheduled for deletion today.")
            )
            return

        for user in expired_users:
            email = user.email
            username = user.username

            # Send the Farewell Email
            send_mail(
                subject="Your DevHuddle Account has been Deleted",
                message=f"Hello {username},\n\nYour 3-day grace period has ended. Your DevHuddle account and all associated data have been permanently deleted from our servers.\n\nWe are sorry to see you go.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

            # Nuke the account (Cascades to all their posts/comments)
            user.delete()
            self.stdout.write(self.style.WARNING(f"Permanently deleted @{username}"))

        self.stdout.write(
            self.style.SUCCESS(f"Sweep complete. {count} accounts purged.")
        )
