from django.core.exceptions import ValidationError
import os


def validate_file_size(file):
    filesize = file.size
    limit_mb = 5  # 5MB
    if filesize > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb}MB.")


def validate_image_extension(file):
    extension = os.path.splitext(file.name)[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png"]
    if extension not in valid_extensions:
        raise ValidationError(
            f"Unsupported file format. Only jpeg, jpg, png are allowed. Current: {extension}"
        )
