# /users/views.py

import stripe
from datetime import timedelta
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import (
    Count,
    F,
    ExpressionWrapper,
    IntegerField,
    Case,
    When,
)
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
)
from feed.models import Notification, Post
from .models import (
    CustomUser,
    Project,
    Experience,
    Skill,
)
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProjectForm,
    ExperienceForm,
    SkillUpdateForm,
)


# ==========================================
# ACCOUNTS HANDLING
# ==========================================
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/auth/signup.html"


# ==========================================
# PROFILE (DASHBOARD)
# ==========================================
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile/edit.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "users/profile/delete.html"
    success_url = reverse_lazy("signup")

    def get_object(self):
        return self.request.user


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile/view.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context["stat_posts"] = Post.objects.filter(author=user).count()
        context["stat_projects"] = user.projects.count()
        impact_agg = Post.objects.filter(author=user).aggregate(
            total_likes=Count("likes")
        )
        context["stat_impact"] = impact_agg["total_likes"] or 0

        # Global Leaderboard Rank
        if user.role == "dev":
            # Execute the same Dev Score algorithm used in the Directory/Developers
            ranked_devs = (
                CustomUser.objects.filter(role="dev")
                .annotate(
                    follower_count=Count("followers", distinct=True),
                    project_count=Count("projects", distinct=True),
                    premium_bonus=Case(
                        When(premium_expires_at__gt=now(), then=50),
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
                .order_by("-dev_score", "-date_joined")
            )

            dev_list = list(ranked_devs.values_list("id", flat=True))
            try:
                context["stat_rank"] = f"{dev_list.index(user.id) + 1}"
            except ValueError:
                context["stat_rank"] = "N/A"
        else:
            context["stat_rank"] = "Org"

        # Profile Strength Index (%)
        strength = 0
        if user.avatar:
            strength += 20
        if user.bio:
            strength += 20
        if user.skills.exists():
            strength += 20
        if user.projects.exists():
            strength += 20
        if user.github_url or user.linkedin_url or user.portfolio_url:
            strength += 20
        context["stat_active"] = strength

        return context


@login_required
def follow_user(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    currentUser = request.user

    if currentUser == target_user:
        return JsonResponse({"error": "You cannot follow yourself"}, status=400)

    if currentUser.following.filter(pk=target_user.pk).exists():
        currentUser.following.remove(target_user)
        is_following = False
    else:
        currentUser.following.add(target_user)
        is_following = True

    return JsonResponse(
        {
            "is_following": is_following,
            "followers_count": target_user.followers.count(),
            "following_count": target_user.following.count(),
        }
    )


@login_required
def toggle_block(request, username):
    target_user = get_object_or_404(CustomUser, username=username)

    if target_user != request.user:
        if request.user.blocked_users.filter(pk=target_user.pk).exists():
            request.user.blocked_users.remove(target_user)
            messages.success(request, f"You unblocked @{target_user.username}.")
        else:
            request.user.blocked_users.add(target_user)
            # 🛡️ Force mutual unfollow
            request.user.following.remove(target_user)
            target_user.following.remove(request.user)
            messages.warning(
                request,
                f"You blocked @{target_user.username}. Their content is now hidden.",
            )

    return redirect(request.META.get("HTTP_REFERER", "home"))


# ==========================================
# PORTFOLIO (PROJECTS) WORKSPACE
# ==========================================
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "users/profile/project_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  # Bind to current user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "users/profile/project_form.html"

    def test_func(self):
        # Strict RBAC: Only the owner can edit
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "users/profile/proj_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


# ==========================================
# EXPERIENCE WORKSPACE
# ==========================================
class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = "users/profile/experience_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = "users/profile/experience_form.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


class ExperienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Experience
    template_name = "users/profile/exp_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


# ==========================================
# USER SKILLS
# ==========================================
class SkillUpdateView(LoginRequiredMixin, FormView):
    template_name = "users/profile/skill_form.html"
    form_class = SkillUpdateForm

    def get_initial(self):
        current_skills = self.request.user.skills.all().values_list("name", flat=True)
        return {"skills": ", ".join(current_skills)}

    def form_valid(self, form):
        skill_string = form.cleaned_data.get("skills", "")
        skill_names = [name.strip() for name in skill_string.split(",") if name.strip()]
        skill_objs = []
        for name in skill_names:
            formatted_name = name.title()
            obj, created = Skill.objects.get_or_create(name=formatted_name)
            skill_objs.append(obj)
        self.request.user.skills.set(skill_objs)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_profile", kwargs={"username": self.request.user.username})


# ==========================================
# THE DISCOVERY ENGINE (DEVELOPER DIRECTORY)
# ==========================================
class DeveloperDirectoryView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "pages/developers.html"
    context_object_name = "developers"
    paginate_by = 12

    def get_queryset(self):
        # Base Query: Only show Developers (hide clients/orgs from this specific list)
        queryset = CustomUser.objects.filter(role="dev")

        # Filter by Skill (if requested via URL ?skill=Python)
        skill_filter = self.request.GET.get("skill")
        if skill_filter:
            queryset = queryset.filter(skills__name__iexact=skill_filter)

        # The Ranking Algorithm
        queryset = (
            queryset.annotate(
                follower_count=Count("followers", distinct=True),
                project_count=Count("projects", distinct=True),
            )
            .annotate(
                premium_bonus=Case(
                    When(premium_expires_at__gt=now(), then=20),
                    default=0,
                    output_field=IntegerField(),
                )
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
            .order_by("-dev_score", "-date_joined")
        )

        # Prefetch skills to prevent N+1 queries in the template
        return queryset.prefetch_related("skills")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass top 15 most popular skills to the template for the filter sidebar
        context = super().get_context_data(**kwargs)
        context["popular_skills"] = (
            Skill.objects.annotate(user_count=Count("users"))
            .filter(user_count__gt=0)
            .order_by("-user_count")[:10]
        )

        # Pass the current filter to highlight the active tab
        context["current_skill"] = self.request.GET.get("skill", "")
        return context


class NetworkView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile/network.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context["followers"] = user.followers.all()
        context["following"] = user.following.all()

        # Security: Only allow the owner to see their blocked list
        if self.request.user == user:
            context["blocked_users"] = user.blocked_users.all()

        return context


# ==========================================
# THE MONETIZATION STOREFRONT
# ==========================================
class StoreView(LoginRequiredMixin, TemplateView):
    template_name = "pages/store.html"


# Configuring the Stripe library with secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item = request.POST.get("item")
        domain = request.build_absolute_uri("/")[
            :-1
        ]  # Gets local or production domain dynamically

        # Define the dynamic pricing based on what the user clicked
        if item == "premium":
            name = "DevHuddle Pro (30 Days)"
            price = 1500  # Stripe calculates in cents ($15.00)
        elif item == "boost_1":
            name = "1x Profile Boost"
            price = 200  # $2.00
        elif item == "boost_5":
            name = "5x Profile Boosts"
            price = 800  # $8.00
        else:
            messages.error(request, "Invalid item selected.")
            return redirect("store")

        # Create the Stripe Checkout Session
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": name},
                            "unit_amount": price,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                # Pass the session_id back to success view to verify the payment
                success_url=domain
                + reverse("checkout_success")
                + f"?session_id={{CHECKOUT_SESSION_ID}}&item={item}",
                cancel_url=domain + reverse("store"),
            )
            # Redirect the user to the secure Stripe-hosted payment page
            return redirect(session.url)

        except Exception as e:
            messages.error(request, f"Stripe Gateway Error: {str(e)}")
            return redirect("store")


class PaymentSuccessView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        item = request.GET.get("item")
        user = request.user

        if not session_id or not item:
            return redirect("store")

        try:
            # Verify the payment with Stripe's servers to prevent users from faking the URL
            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                # Fulfill the Order!
                if item == "premium":
                    if user.is_premium:
                        user.premium_expires_at += timedelta(days=30)
                        messages.success(
                            request,
                            f"Payment successful! Pro extended to {user.premium_expires_at.strftime('%b %d, %Y')}.",
                        )
                    else:
                        user.premium_expires_at = now() + timedelta(days=30)
                        messages.success(
                            request, "Payment successful! DevHuddle Pro activated."
                        )
                        Notification.objects.create(
                            recipient=user, actor=user, verb="premium"
                        )

                elif item == "boost_1":
                    user.profile_boosts += 1
                    messages.success(request, "Payment successful! 1 Boost added.")

                elif item == "boost_5":
                    user.profile_boosts += 5
                    messages.success(request, "Payment successful! 5 Boosts added.")

                user.save()
            else:
                messages.warning(request, "Payment has not been completed.")

        except stripe.error.StripeError:
            messages.error(request, "Could not verify payment with Stripe.")

        return redirect("user_profile", username=user.username)


class BoostUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        target_user = get_object_or_404(CustomUser, username=username)

        if request.user == target_user:
            messages.error(request, "You cannot boost yourself here. Use the Store.")
        elif request.user.profile_boosts > 0:
            # Transfer the boost
            request.user.profile_boosts -= 1
            request.user.save()
            target_user.profile_boosts += 1
            target_user.save()

            messages.success(
                request, f"You used 1 Boost to amplify {target_user.username}!"
            )
            Notification.objects.create(
                recipient=target_user, actor=request.user, verb="boost"
            )
        else:
            messages.error(request, "You have 0 Boosts. Buy more in the Store!")

        return redirect("user_profile", username=username)
