from django.contrib import admin
from django.urls import path
from feed import views
# from .views import about_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("post/new/", views.PostCreateView.as_view(), name="post_new"),
]
