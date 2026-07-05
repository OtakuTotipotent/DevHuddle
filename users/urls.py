# /users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    NetworkView,
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
    StoreView,
    CreateStripeCheckoutSessionView,
    PaymentSuccessView,
    BoostUserView,
    toggle_block,
)
from .forms import CustomPasswordResetForm, CustomSetPasswordForm


urlpatterns = [
    path(
        # Accounts
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
    # Password Reset Pipeline
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/auth/password_reset_form.html",
            form_class=CustomPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/auth/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
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
    path(
        "profile/<str:username>/block/",
        toggle_block,
        name="toggle_block",
    ),
    path(
        "profile/<str:username>/network/",
        NetworkView.as_view(),
        name="user_network",
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
    #
    # Monetization
    path(
        "store/",
        StoreView.as_view(),
        name="store",
    ),
    path(
        "store/checkout/",
        CreateStripeCheckoutSessionView.as_view(),
        name="checkout",
    ),
    path(
        "store/checkout/success/",
        PaymentSuccessView.as_view(),
        name="checkout_success",
    ),
    path(
        "profile/<str:username>/boost/",
        BoostUserView.as_view(),
        name="boost_user",
    ),
]
