from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count, ExpressionWrapper, IntegerField, F
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views import View

from .models import Comment, Post, Notification
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
        if request.user != post.author:  # Don't notify if I like my own post
            Notification.objects.create(
                recipient=post.author, actor=request.user, verb="like", post=post
            )
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

    return render(request, "pages/search_results.html", context)


class HomePageView(ListView):
    model = Post
    template_name = "pages/home.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.all().order_by("-created_at")

        feed_type = self.request.GET.get("feed", "fellows")
        queryset = Post.objects.annotate(
            like_count=Count("likes", distinct=True),
            comment_count=Count("comments", distinct=True),
        )

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

        elif feed_type == "global":  # Everything: The Ranking Algorithm
            # Score = (Likes * 2) + (Comments * 3) + (Boosts * 5)
            queryset = (
                queryset.filter(post_type__in=["huddle", "job", "ad"])
                .annotate(
                    engagement_score=ExpressionWrapper(
                        (F("like_count") * 2) + (F("comment_count") * 3),
                        output_field=IntegerField(),
                    )
                )
                .order_by("-is_boosted", "-engagement_score", "-created_at")
            )
            return queryset

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
    template_name = "pages/about.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "components/posts/create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "components/posts/update.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "components/posts/delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = "components/posts/view.html"
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
        # Handle nested replies
        parent_id = self.request.POST.get("parent_id")
        if parent_id:
            form.instance.parent_id = parent_id
        comment = form.save()
        # Trigger Notification System
        if self.request.user != form.instance.post.author:
            Notification.objects.create(
                recipient=form.instance.post.author,
                actor=self.request.user,
                verb="comment",
                post=form.instance.post,
            )
        if parent_id and self.request.user != comment.parent.author:
            Notification.objects.create(
                recipient=comment.parent.author,
                actor=self.request.user,
                verb="reply",
                post=form.instance.post,
            )
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["body"]
    template_name = "components/comments/edit.html"

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user and not comment.is_deleted

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        # Soft-delete mechanics: Flag it and overwrite the text for privacy
        comment.is_deleted = True
        comment.body = "This message was deleted by the user."
        comment.save()
        return redirect("post_detail", pk=comment.post.pk)

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        return comment.author == self.request.user and not comment.is_deleted


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "pages/notifications.html"
    context_object_name = "notifications"

    def get(self, request, *args, **kwargs):
        unread_qs = Notification.objects.filter(recipient=request.user, is_read=False)
        self.just_read_ids = list(unread_qs.values_list("id", flat=True))
        unread_qs.update(is_read=True)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by(
            "-created_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["just_read_ids"] = self.just_read_ids
        return context
