from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Count,
    F,
    ExpressionWrapper,
    IntegerField,
    Case,
    When,
)
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import (
    CustomUser,
    Project,
    Experience,
    Skill,
)
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProjectForm,
    ExperienceForm,
    SkillUpdateForm,
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
    template_name = "users/profile/proj_delete.html"

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
    template_name = "users/profile/exp_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


# ==========================================
# USER SKILLS
# ==========================================
class SkillUpdateView(LoginRequiredMixin, FormView):
    template_name = "users/profile/skill_form.html"
    form_class = SkillUpdateForm

    def get_initial(self):
        current_skills = self.request.user.skills.all().values_list("name", flat=True)
        return {"skills": ", ".join(current_skills)}

    def form_valid(self, form):
        skill_string = form.cleaned_data.get("skills", "")
        skill_names = [name.strip() for name in skill_string.split(",") if name.strip()]
        skill_objs = []
        for name in skill_names:
            formatted_name = name.title()
            obj, created = Skill.objects.get_or_create(name=formatted_name)
            skill_objs.append(obj)
        self.request.user.skills.set(skill_objs)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


# ==========================================
# THE DISCOVERY ENGINE (DEVELOPER DIRECTORY)
# ==========================================
class DeveloperDirectoryView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "pages/developers.html"
    context_object_name = "developers"
    paginate_by = 12

    def get_queryset(self):
        # Base Query: Only show Developers (hide clients/orgs from this specific list)
        queryset = CustomUser.objects.filter(role="dev")

        # Filter by Skill (if requested via URL ?skill=Python)
        skill_filter = self.request.GET.get("skill")
        if skill_filter:
            queryset = queryset.filter(skills__name__iexact=skill_filter)

        # The Ranking Algorithm
        queryset = (
            queryset.annotate(
                follower_count=Count("followers", distinct=True),
                project_count=Count("projects", distinct=True),
            )
            .annotate(
                premium_bonus=Case(
                    When(is_premium=True, then=20),
                    default=0,
                    output_field=IntegerField(),
                )
            )
            .annotate(
                dev_score=ExpressionWrapper(
                    (F("follower_count") * 2)
                    + (F("project_count") * 3)
                    + (F("profile_boosts") * 7)
                    + F("premium_bonus"),
                    output_field=IntegerField(),
                )
            )
            .order_by("-dev_score", "-date_joined")
        )

        # Prefetch skills to prevent N+1 queries in the template
        return queryset.prefetch_related("skills")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass top 15 most popular skills to the template for the filter sidebar
        context = super().get_context_data(**kwargs)
        context["popular_skills"] = (
            Skill.objects.annotate(user_count=Count("users"))
            .filter(user_count__gt=0)
            .order_by("-user_count")[:10]
        )

        # Pass the current filter to highlight the active tab
        context["current_skill"] = self.request.GET.get("skill", "")
        return context
