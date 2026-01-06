from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    clear_image = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Post
        fields = ["body", "image", "post_type"]

        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "w-full bg-gray-700 text-white rounded-lg p-2 my-2 border border-gray-600 focus:border-blue-500 outline-none",
                    "placeholder": "What's on your mind, developer?",
                    "rows": 4,
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-400 file:mr-4 file:py-1 file:px-3 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer mt-2 file:cursor-pointer cursor-pointer"
                }
            ),
            "post_type": forms.Select(
                attrs={
                    "class": "bg-gray-700 text-white border border-gray-500 rounded-full px-2 pt-[1px] pb-[3px] mx-6 my-5 outline-none cursor-pointer text-center"
                }
            ),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        if self.cleaned_data.get("clear_image"):
            post.image.delete()
            post.image = None
        if commit:
            post.save()

        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-700 text-white rounded-lg p-3 border border-gray-600 focus:border-blue-500 outline-none placeholder-gray-400",
                    "placeholder": "What do you think?...",
                }
            )
        }
