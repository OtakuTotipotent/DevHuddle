from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy

from .models import Post, Comment
from .forms import PostForm, CommentForm


# FUNCTION-BASED VIEWS


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({"liked": liked, "count": post.likes.count()})


# CLASS-BASED VIEWS


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


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_update.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the form to the template
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Connect the comment to the User and the Post
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return super().form_valid(form)
