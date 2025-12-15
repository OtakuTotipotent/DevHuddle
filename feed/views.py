from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


# Create your views here.
class HomePageView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 5


class AboutPageView(TemplateView):
    template_name = "about.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
