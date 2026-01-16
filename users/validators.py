import re
import os
from django.core.exceptions import ValidationError


def validate_file_size(file):
    """
    Validator to ensure the uploaded media is not bulky in size.
    """
    filesize = file.size
    limit_mb = 5  # 5MB
    if filesize > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb}MB.")


def validate_image_extension(file):
    """
    Validator to ensure the uploaded media is a valid image.
    """
    extension = os.path.splitext(file.name)[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png"]
    if extension not in valid_extensions:
        raise ValidationError(
            f"Unsupported file format. Only jpeg, jpg, png are allowed. Current: {extension}"
        )


def validate_username(value):
    RESERVED_USERNAMES = [
        "admin",
        "superuser",
        "staff",
        "login",
        "logout",
        "signup",
        "register",
        "api",
        "media",
        "static",
        "assets",
        "help",
        "about",
        "contact",
        "terms",
        "privacy",
        "settings",
        "profile",
        "dashboard",
        "feed",
        "notifications",
        "messages",
        "search",
        "explore",
        "huddle",
        "dev",
        "root",
        "support",
    ]

    # Reserved Words
    if value.lower() in RESERVED_USERNAMES:
        raise ValidationError(f"'{value}' is a reserved system keyword.")

    # Allowed Characters (Alphanumeric, dot, underscore)
    if not re.match("^(?!.*[._]{2})[a-zA-Z0-9._]+$", value):
        raise ValidationError(
            "Username can only contain letters, numbers, dots (.), and underscores (_). No consecutive dots or underscores allowed.",
        )
    # Specific Dangerous Patterns
    if "devhuddle" in value.lower():
        raise ValidationError("Username cannot contain the platform name.")
