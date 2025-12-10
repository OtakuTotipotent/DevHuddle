from django.contrib import admin
from django.urls import path, include
from users.views import SignUpView, ProfileUpdateView
from django.conf import settings
from django.conf.urls.static import static

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
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]

# ONLY FOR DEVELOPMENT PURPOSES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
