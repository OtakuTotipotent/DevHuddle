from django.urls import path
from .views import SignUpView, ProfileUpdateView, UserProfileView, ProfileDeleteView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    #
    # Profile related routes
    path("edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("delete/", ProfileDeleteView.as_view(), name="profile_delete"),
    #
    # Public profile route | "/u/otaku/"
    path("profile/<str:username>/", UserProfileView.as_view(), name="user_profile"),
]
