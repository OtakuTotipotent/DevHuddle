# DevHuddle/users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Skill, Project, Experience
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
        fields = ("username", "email", "role")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 4 characters long.")

        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full bg-gray-700 text-white border border-gray-600 rounded-full px-4 pt-1 pb-2 focus:outline-none focus:border-blue-500 mb-2 placeholder:text-xs",
                    "placeholder": f"Enter {field_name} here...",
                }
            )

            if field_name == "role":
                field.widget.attrs.update(
                    {
                        "class": "bg-gray-700 text-white border border-gray-600 rounded-full px-4 pt-1 pb-2 focus:outline-none focus:border-blue-500 mb-2"
                    }
                )

            if field_name == "password1":
                field.widget.attrs.update({"placeholder": "Create a new password..."})

            if field_name == "password2":
                field.widget.attrs.update(
                    {"placeholder": "Type again your password here..."}
                )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "live_url", "github_url", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                    "placeholder": "e.g. DevHuddle AI Video Editor",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                    "rows": 4,
                    "placeholder": "Describe the architecture and your role...",
                }
            ),
            "live_url": forms.URLInput(
                attrs={
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                    "placeholder": "https://...",
                }
            ),
            "github_url": forms.URLInput(
                attrs={
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                    "placeholder": "https://github.com/...",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer mt-2"
                }
            ),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "company",
            "role",
            "start_date",
            "end_date",
            "is_current",
            "description",
        ]
        widgets = {
            "company": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                    "placeholder": "e.g. Google",
                }
            ),
            "role": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                    "placeholder": "e.g. Senior Backend Engineer",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                }
            ),
            "is_current": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 rounded border-gray-700 text-blue-600 focus:ring-blue-500 bg-gray-900"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                    "rows": 4,
                    "placeholder": "Key achievements...",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get("is_current")
        end_date = cleaned_data.get("end_date")

        if is_current:
            cleaned_data["end_date"] = None
        elif not is_current and not end_date:
            self.add_error(
                "end_date", 'Please provide an end date, or check "is current".'
            )

        return cleaned_data


class SkillUpdateForm(forms.Form):
    skills = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-gray-900 text-white rounded-lg p-3 border border-gray-700 focus:border-blue-500 outline-none",
                "placeholder": "e.g. Python, Django, Docker, ReactJS",
            }
        ),
        help_text="Separate skills with commas. We will format them for you.",
        required=False,
    )
