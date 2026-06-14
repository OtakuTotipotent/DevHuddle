from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView,
    ProfileUpdateView,
    UserProfileView,
    ProfileDeleteView,
    follow_user,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ExperienceCreateView,
    ExperienceUpdateView,
    ExperienceDeleteView,
    SkillUpdateView,
    DeveloperDirectoryView,
)


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/auth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "signup/",
        SignUpView.as_view(),
        name="signup",
    ),
    #
    # Profile related routes
    path(
        "edit/",
        ProfileUpdateView.as_view(),
        name="profile_edit",
    ),
    path(
        "delete/",
        ProfileDeleteView.as_view(),
        name="profile_delete",
    ),
    #
    # Public profile route | "/u/otaku/"
    path(
        "profile/<str:username>/",
        UserProfileView.as_view(),
        name="user_profile",
    ),
    path(
        "profile/skills/edit/",
        SkillUpdateView.as_view(),
        name="skill_edit",
    ),
    #
    # Developers on Search
    path(
        "developers/",
        DeveloperDirectoryView.as_view(),
        name="developer_directory",
    ),
    #
    # Social routes
    path(
        "follow/<str:username>/",
        follow_user,
        name="follow_user",
    ),
    #
    # Portfolio Workspaces
    path(
        "profile/project/new/",
        ProjectCreateView.as_view(),
        name="project_create",
    ),
    path(
        "profile/project/<int:pk>/edit/",
        ProjectUpdateView.as_view(),
        name="project_edit",
    ),
    path(
        "profile/project/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project_delete",
    ),
    #
    # Experience Workspaces
    path(
        "profile/experience/new/",
        ExperienceCreateView.as_view(),
        name="experience_create",
    ),
    path(
        "profile/experience/<int:pk>/edit/",
        ExperienceUpdateView.as_view(),
        name="experience_edit",
    ),
    path(
        "profile/experience/<int:pk>/delete/",
        ExperienceDeleteView.as_view(),
        name="experience_delete",
    ),
]
