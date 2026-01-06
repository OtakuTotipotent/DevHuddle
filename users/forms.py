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
            "role",
            "tech_stack",
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
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full bg-gray-700 text-white border border-gray-600 rounded-full px-3 pt-1 pb-2 focus:outline-none focus:border-blue-500 mb-2",
                    "placeholder": f"Enter {field_name} here...",
                }
            )

            if field_name == "role":
                field.widget.attrs.update(
                    {
                        "class": "bg-gray-700 text-white border border-gray-600 rounded-full px-3 pt-1 pb-2 focus:outline-none focus:border-blue-500 mb-2"
                    }
                )

            if field_name == "bio":
                field.widget.attrs.update(
                    {
                        "class": "w-full bg-gray-700 text-white border border-gray-600 rounded-lg p-3 focus:outline-none focus:border-blue-500 mb-2",
                        "rows": 4,
                    }
                )

            if field_name == "avatar":
                field.widget.attrs.update(
                    {
                        "class": "block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:cursor-pointer cursor-pointer mt-2"
                    }
                )

            if field_name == "password":
                self.fields["password"].widget = forms.HiddenInput()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role", "tech_stack")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full bg-gray-700 text-white border border-gray-600 rounded-full px-4 pt-1 pb-2 focus:outline-none focus:border-blue-500 mb-2 placeholder:text-xs",
                    "placeholder": f"Enter {field_name} here...",
                }
            )

            if field_name == "tech_stack":
                field.widget.attrs["placeholder"] = (
                    "MERN, SpringBoot, Django, Laravel, AWS, DBMS, AI..."
                )

            if field_name == "role":
                field.widget.attrs.update(
                    {
                        "class": "bg-gray-700 text-white border border-gray-600 rounded-full px-4 pt-1 pb-2 focus:outline-none focus:border-blue-500 mb-2"
                    }
                )

            if "password" in field_name:
                field.widget.attrs["class"] += " remove-eye-icon"
