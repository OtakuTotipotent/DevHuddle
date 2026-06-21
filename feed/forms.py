# /feed/forms.py

from django import forms
from .models import Post, Comment, Proposal


class PostForm(forms.ModelForm):
    clear_image = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Post
        fields = ["post_type", "body", "image", "deadline", "target_url", "tags"]

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
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "bg-gray-700 text-white border border-gray-500 rounded-full py-1 px-4 focus:border-blue-500 col-span-2 outline-none",
                }
            ),
            "target_url": forms.URLInput(
                attrs={
                    "placeholder": "https://...",
                    "class": "bg-gray-700 text-white border border-gray-500 rounded-full py-1 px-4 focus:border-blue-500 col-span-2 outline-none",
                }
            ),
            "tags": forms.TextInput(
                attrs={
                    "placeholder": "e.g. #Python, #Remote",
                    "class": "bg-gray-700 text-white border border-gray-500 rounded-full py-1 px-4 focus:border-blue-500 col-span-2 outline-none",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # RBAC ENFORCEMENT: Restrict post types based on role
        if user and user.role == "dev":
            # Devs can ONLY post standard Huddles
            self.fields["post_type"].choices = [("huddle", "Huddle")]
        elif user and user.role in ["client", "org"]:
            # Clients/Orgs can post Huddles, Jobs, and Ads
            pass

    def save(self, commit=True):
        post = super().save(commit=False)
        if self.cleaned_data.get("clear_image"):
            post.image.delete()
            post.image = None
        if commit:
            post.save()
        return post


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ["cover_letter", "bid_amount"]
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "w-full bg-gray-700 text-white rounded-lg p-3 my-2 border border-gray-600 focus:border-blue-500 outline-none",
                    "placeholder": "Explain your tech stack and why you fit this project...",
                    "rows": 5,
                    # "style": "resize: none;",
                }
            ),
            "bid_amount": forms.NumberInput(
                attrs={
                    "class": "w-full bg-gray-700 text-white border border-gray-600 rounded-lg p-3 focus:outline-none focus:border-blue-500",
                    "placeholder": "e.g. 500.00",
                    "step": "0.01",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-700 text-white rounded-lg p-3 border border-gray-600 focus:border-blue-500 outline-none placeholder-gray-400",
                    "placeholder": "What do you think?",
                }
            )
        }
