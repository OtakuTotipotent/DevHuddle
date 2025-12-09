from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "w-full bg-gray-700 text-white rounded-lg p-4 border border-gray-600 focus:border-blue-500",
                    "placeholder": "What's on your mind?",
                    "rows": 3,
                }
            )
        }
