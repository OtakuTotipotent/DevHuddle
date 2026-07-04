# /feed/views.py

from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, F, Count, ExpressionWrapper, IntegerField, Case, When
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from users.models import CustomUser, Project
from .models import Bookmark, Comment, Post, Notification, Proposal, Message, Report
from .forms import PostForm, CommentForm, ProposalForm


# ==========================================
# HELPER FUNCTIONS
# ==========================================


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
    query = request.GET.get("q", "").strip()

    users = []
    huddles = []
    jobs = []

    if query:
        users = (
            CustomUser.objects.annotate(
                follower_count=Count("followers", distinct=True)
            )
            .filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(bio__icontains=query)
                | Q(skills__name__icontains=query)
            )
            .distinct()
            .order_by("-follower_count")[:10]
        )

        base_posts = (
            Post.objects.filter(Q(body__icontains=query) | Q(tags__icontains=query))
            .select_related("author")
            .annotate(like_count=Count("likes", distinct=True))
        )

        huddles = base_posts.filter(post_type="huddle").order_by(
            "-like_count", "-created_at"
        )[:15]
        jobs = base_posts.filter(post_type="job").order_by("-created_at")[:10]

    context = {
        "query": query,
        "users": users,
        "huddles": huddles,
        "jobs": jobs,
    }
    return render(request, "pages/search_results.html", context)


@login_required
def toggle_bookmark(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

        if not created:
            bookmark.delete()
            messages.info(request, "Post removed from your bookmarks.")
        else:
            messages.success(request, "Post saved to your bookmarks!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def submit_report(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)

        report, created = Report.objects.get_or_create(reporter=request.user, post=post)

        if created:
            messages.success(
                request, "Report submitted to DevHuddle moderators securely."
            )

            Notification.objects.create(
                recipient=request.user,
                actor=request.user,
                verb="report_submitted",
                post=post,
            )

            # set actor=post.author so the reporter's identity remains absolutely private.
            Notification.objects.create(
                recipient=post.author,
                actor=post.author,
                verb="post_reported",
                post=post,
            )

        else:
            messages.info(request, "You have already reported this post.")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


# ==========================================
# BASE PAGES
# ==========================================


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

        # LEFT SIDEBAR: Available Jobs
        context["sidebar_jobs"] = (
            Post.objects.filter(post_type="job")
            .select_related("author")
            .order_by("-created_at")[:5]
        )

        # LEFT SIDEBAR: Explore Projects
        context["sidebar_projects"] = (
            Project.objects.select_related("user")
            .prefetch_related("user__skills")
            .order_by("-created_at")[:4]
        )

        # RIGHT SIDEBAR: Popular Developers
        if self.request.user.is_authenticated:
            context["who_to_follow"] = (
                CustomUser.objects.annotate(
                    follower_count=Count("followers", distinct=True),
                    project_count=Count("projects", distinct=True),
                    premium_bonus=Case(
                        When(is_premium=True, then=50),
                        default=0,
                        output_field=IntegerField(),
                    ),
                )
                .annotate(
                    dev_score=ExpressionWrapper(
                        (F("follower_count") * 2)
                        + (F("project_count") * 3)
                        + (F("profile_boosts") * 7)
                        + F("premium_bonus"),
                        output_field=IntegerField(),
                    )
                )
                .order_by("-dev_score", "-date_joined")[:10]
            )

        return context


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


# ==========================================
# DASHBOARDS
# ==========================================


class ClientDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "pages/client_dashboard.html"
    context_object_name = "jobs"

    def test_func(self):
        # RBAC: Only Clients and Orgs can access the hirer dashboard
        return self.request.user.role in ["client", "org"]

    def get_queryset(self):
        """Performance optimization: prefetch_related stops N+1 queries when looping through proposals in the template"""
        return (
            Post.objects.filter(author=self.request.user, post_type="job")
            .prefetch_related("proposals__applicant")
            .order_by("-created_at")
        )


class DeveloperDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "pages/dev_dashboard.html"
    context_object_name = "proposals"

    def test_func(self):
        # RBAC: Only 'dev' roles can access the applicant dashboard
        return self.request.user.role == "dev"

    def get_queryset(self):
        """Fetch proposals created by this dev, fetch related Job and Author for performance"""
        return (
            Proposal.objects.filter(applicant=self.request.user)
            .select_related("job", "job__author")
            .order_by("-created_at")
        )


class ProposalCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = "components/posts/submit_proposal.html"

    def test_func(self):
        # RBAC: Only 'dev' roles can apply for jobs
        return self.request.user.role == "dev"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the specific job to the template
        context["job"] = get_object_or_404(Post, pk=self.kwargs["pk"], post_type="job")
        return context

    def form_valid(self, form):
        job = get_object_or_404(Post, pk=self.kwargs["pk"], post_type="job")

        # Security: Prevent duplicate applications
        if Proposal.objects.filter(job=job, applicant=self.request.user).exists():
            messages.error(self.request, "You have already applied to this job.")
            return redirect("post_detail", pk=job.pk)

        form.instance.applicant = self.request.user
        form.instance.job = job
        # proposal = form.save()
        form.save()

        # NOTIFICATION: Notify the Client that a Dev applied
        Notification.objects.create(
            recipient=job.author,
            actor=self.request.user,
            verb="hire",
            post=job,
        )

        messages.success(self.request, "Your proposal has been submitted successfully.")
        return redirect("post_detail", pk=job.pk)


class ProposalActionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk, action, *args, **kwargs):
        proposal = get_object_or_404(Proposal, pk=pk)

        # State Mutation
        if action == "accept":
            proposal.status = "accepted"
            verb = "accept"
            messages.success(
                request,
                f"You accepted the proposal from {proposal.applicant.username}.",
            )
        elif action == "reject":
            proposal.status = "rejected"
            verb = "reject"
            messages.error(
                request,
                f"You declined the proposal from {proposal.applicant.username}.",
            )
        else:
            return redirect("client_dashboard")

        proposal.save()

        # Alert the Developer of the decision
        Notification.objects.create(
            recipient=proposal.applicant,
            actor=request.user,
            verb=verb,
            post=proposal.job,
        )

        return redirect("client_dashboard")

    def test_func(self):
        """Strict RBAC Security: Only the actual creator of the job can accept/reject its proposals"""
        proposal = get_object_or_404(Proposal, pk=self.kwargs["pk"])
        return self.request.user == proposal.job.author


# ==========================================
# FEED POSTS
# ==========================================


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "components/posts/create.html"
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        requested_type = self.request.GET.get("type")
        if requested_type in ["huddle", "job", "ad"]:
            initial["post_type"] = requested_type
        return initial

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
        comment.save()
        return redirect("post_detail", pk=comment.post.pk)

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        return comment.author == self.request.user and not comment.is_deleted


# ==========================================
# NOTIFICATION SYSTEM
# ==========================================


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


# ==========================================
# Messaging System
# ==========================================


class InboxView(LoginRequiredMixin, TemplateView):
    template_name = "pages/inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        all_messages = (
            Message.objects.filter(Q(sender=user) | Q(recipient=user))
            .order_by("-created_at")
            .select_related("sender", "recipient")
        )

        conversations = []
        seen_users = set()

        for msg in all_messages:
            contact = msg.recipient if msg.sender == user else msg.sender
            if contact not in seen_users:
                seen_users.add(contact)
                conversations.append(
                    {
                        "contact": contact,
                        "last_message": msg,
                        "unread": not msg.is_read and msg.recipient == user,
                    }
                )

        context["conversations"] = conversations
        return context


class ChatThreadView(LoginRequiredMixin, View):
    def get(self, request, username):
        contact = get_object_or_404(CustomUser, username=username)

        Message.objects.filter(
            sender=contact, recipient=request.user, is_read=False
        ).update(is_read=True)

        messages = Message.objects.filter(
            Q(sender=request.user, recipient=contact)
            | Q(sender=contact, recipient=request.user)
        ).order_by("created_at")

        return render(
            request,
            "pages/chat_thread.html",
            {"contact": contact, "messages": messages},
        )

    def post(self, request, username):
        contact = get_object_or_404(CustomUser, username=username)
        body = request.POST.get("body", "").strip()

        if body:
            Message.objects.create(sender=request.user, recipient=contact, body=body)
            Notification.objects.create(
                recipient=contact, actor=request.user, verb="dm"
            )

        return redirect("chat_thread", username=username)


# ==========================================
# TRUST & SAFETY CENTER | REPORTING SYSTEM
# ==========================================


class ModerationDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "pages/moderation_dashboard.html"
    context_object_name = "flagged_posts"

    def test_func(self):
        # SECURITY: Only Staff or Superusers can access
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        return (
            Post.objects.filter(reports__is_resolved=False)
            .annotate(
                active_reports=Count("reports", filter=Q(reports__is_resolved=False))
            )
            .distinct()
            .prefetch_related("author")
            .order_by("-active_reports", "-created_at")
        )


class ModerationActionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, pk, action):
        post_obj = get_object_or_404(Post, pk=pk)

        if action == "dismiss":
            # Bulk update all reports for this specific post to 'resolved'
            post_obj.reports.filter(is_resolved=False).update(is_resolved=True)
            messages.success(
                request, f"Cleared all reports for post by @{post_obj.author.username}."
            )
        elif action == "delete":
            # Nuke the post overall
            post_obj.delete()
            messages.success(
                request,
                "Violating post has been permanently deleted from the ecosystem.",
            )

        return redirect("moderation_dashboard")


# ==========================================
# ECOSYSTEM DISCOVERY (JOBS, CLIENTS, PROJECTS)
# ==========================================


class EcosystemDiscoveryView(LoginRequiredMixin, TemplateView):
    template_name = "pages/jobs_clients.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch Active Jobs (Latest 12)
        context["jobs"] = (
            Post.objects.filter(post_type="job")
            .select_related("author")
            .order_by("-created_at")[:12]
        )

        # Fetch Top Clients & Orgs (Ranked by number of jobs posted)
        context["clients"] = (
            CustomUser.objects.filter(role__in=["client", "org"])
            .annotate(job_count=Count("post", filter=Q(post__post_type="job")))
            .order_by("-job_count", "-date_joined")[:12]
        )

        # Fetch Featured Projects (Latest 12 with images preferred)
        context["projects"] = Project.objects.select_related("user").order_by(
            F("image").desc(nulls_last=True), "-created_at"
        )[:12]

        return context
