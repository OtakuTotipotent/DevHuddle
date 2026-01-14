from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Only for ADMIN users
    path("admin/", admin.site.urls),
    #
    # Users (Login, Signup, Profiles, Edit/New)
    path("users/", include("users.urls")),
    #
    # Feed (Home, Posts, ...)
    path("", include("feed.urls")),
]

# ONLY FOR DEVELOPMENT PURPOSES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
