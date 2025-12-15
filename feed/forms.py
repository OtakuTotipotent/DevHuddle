from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body", "image"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "w-full bg-gray-700 text-white rounded-lg p-4 border border-gray-600 focus:border-blue-500 outline-none",
                    "placeholder": "What's on your mind, developer?",
                    "rows": 4,
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer mt-2 cursor-pointer"
                }
            ),
        }
