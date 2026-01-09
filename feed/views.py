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
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models import Q, Count

from .models import Post
from users.models import CustomUser
from .forms import PostForm, CommentForm


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


@login_required
def search_results(request):
    query = request.GET.get("q")

    users = []
    posts = []

    if query:
        users = CustomUser.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(tech_stack__icontains=query)
            | Q(bio__icontains=query)
        ).distinct()

        posts = Post.objects.filter(Q(body__icontains=query)).order_by("-created_at")

    context = {"query": query, "users": users, "posts": posts}

    return render(request, "search_results.html", context)


class HomePageView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    paginate_by = 7

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.all().order_by("-created_at")

        feed_type = self.request.GET.get("feed", "fellows")
        queryset = Post.objects.all()

        if feed_type == "fellows":  # Only show standard posts here
            following_ids = self.request.user.following.values_list("id", flat=True)
            queryset = queryset.filter(
                Q(author_id__in=following_ids),
                post_type="huddle",
            )

        elif feed_type == "business":  # Only Jobs/Offers
            queryset = queryset.filter(post_type="job")

        elif feed_type == "ads":  # Show ONLY ads
            queryset = queryset.filter(post_type="ad")

        elif feed_type == "global":  # Everything prioritized by Boost
            queryset = queryset.filter(post_type__in=["huddle", "job"]).order_by(
                "-is_boosted", "-created_at"
            )
            return queryset  # Return early to keep custom ordering

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_feed = self.request.GET.get("feed", "fellows")
        context["current_feed"] = current_feed

        if self.request.user.is_authenticated:
            my_following = self.request.user.following.values_list("id", flat=True)
            context["who_to_follow"] = (
                CustomUser.objects.exclude(id__in=my_following)
                .exclude(id=self.request.user.id)
                .annotate(follower_count=Count("followers"))
                .order_by("-follower_count")[:10]
            )

            return context


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
