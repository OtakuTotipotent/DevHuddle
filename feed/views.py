from django.views.generic import ListView, TemplateView
from . import models


# Create your views here.
class HomePageView(ListView):
    model = models.Post
    template_name = "home.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class AboutPageView(TemplateView):
    template_name = "about.html"
