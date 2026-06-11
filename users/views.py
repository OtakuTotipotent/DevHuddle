from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import CustomUser, Project, Experience
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProjectForm,
    ExperienceForm,
)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/auth/signup.html"


# ==========================================
# PROFILE (DASHBOARD)
# ==========================================
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile/edit.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "users/profile/delete.html"
    success_url = reverse_lazy("signup")

    def get_object(self):
        return self.request.user


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile/view.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"


@login_required
def follow_user(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    currentUser = request.user

    if currentUser == target_user:
        return JsonResponse({"error": "You cannot follow yourself"}, status=400)

    if currentUser.following.filter(pk=target_user.pk).exists():
        currentUser.following.remove(target_user)
        is_following = False
    else:
        currentUser.following.add(target_user)
        is_following = True

    return JsonResponse(
        {
            "is_following": is_following,
            "followers_count": target_user.followers.count(),
            "following_count": target_user.following.count(),
        }
    )


# ==========================================
# PORTFOLIO (PROJECTS) WORKSPACE
# ==========================================
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "users/profile/project_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  # Bind to current user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "users/profile/project_form.html"

    def test_func(self):
        # Strict RBAC: Only the owner can edit
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "users/profile/project_confirm_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


# ==========================================
# EXPERIENCE WORKSPACE
# ==========================================
class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = "users/profile/experience_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = "users/profile/experience_form.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ExperienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Experience
    template_name = "users/profile/experience_confirm_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})
