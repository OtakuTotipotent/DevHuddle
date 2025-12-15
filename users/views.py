from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
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
    ]
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "registration/delete_account.html"
    success_url = reverse_lazy("signup")

    def get_object(self):
        return self.request.user
