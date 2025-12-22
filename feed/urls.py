from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    like_post,
    PostDetailView,
)


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("post/new/", PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/like/<int:pk>/", like_post, name="like_post"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
