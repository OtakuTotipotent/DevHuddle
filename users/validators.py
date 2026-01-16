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
    """
    Validator to ensure the username contains only letters, numbers,
    dot, hyphen, and underscores.
    """
    if not re.match("^(?!.*[.]{2})[A-Za-z0-9._-]+$", value):
        raise ValidationError(
            "Invalid valid username. Only letters, numbers, dot, hyphen and underscores."
        )
