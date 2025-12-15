# DevHuddle/users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "github_url",
            "linkedin_url",
            "twitter_url",
            "stackoverflow_url",
            "portfolio_url",
            "fiver_url",
            "upwork_url",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        generic_class = "w-full bg-gray-700 text-white border border-gray-600 rounded-lg p-3 focus:outline-none focus:border-blue-500 mb-2"
        for field in self.fields.values():
            field.widget.attrs.update({"class": generic_class, "placeholder": " "})

        self.fields["avatar"].widget.attrs.update(
            {
                "class": "block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer mt-2"
            }
        )
        if "password" in self.fields:
            self.fields["password"].widget = forms.HiddenInput()


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
