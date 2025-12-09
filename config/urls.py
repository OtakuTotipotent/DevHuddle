from django.contrib import admin
from django.urls import path, include
from users.views import SignUpView
# from .views import about_view

urlpatterns = [
    path("admin/", admin.site.urls),
    #
    # Built-in Auth (Login, Logout, Password Management)
    path("accounts/", include("django.contrib.auth.urls")),
    #
    # Custom Sign Up
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    #
    # Application URLs
    path("", include("feed.urls")),
]
