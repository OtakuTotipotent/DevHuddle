from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "w-full bg-gray-700 text-white border border-gray-600 rounded-lg p-3 focus:outline-none focus:border-blue-500 mb-2",
                    "placeholder": " ",
                }
            )
