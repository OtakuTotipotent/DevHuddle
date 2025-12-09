from django.urls import path
from .views import HomePageView, AboutPageView, PostCreateView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("post/new/", PostCreateView.as_view(), name="post_new"),
]
