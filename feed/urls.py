from django.urls import path
from .views import (
    ClientDashboardView,
    CommentDeleteView,
    CommentUpdateView,
    DeveloperDashboardView,
    HomePageView,
    AboutPageView,
    NotificationListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ProposalActionView,
    ProposalCreateView,
    like_post,
    PostDetailView,
    search_results,
)


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("post/new/", PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/like/<int:pk>/", like_post, name="like_post"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("search/", search_results, name="search"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("comment/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment_edit"),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"
    ),
    path("job/<int:pk>/apply/", ProposalCreateView.as_view(), name="apply_job"),
    path("dashboard/client/", ClientDashboardView.as_view(), name="client_dashboard"),
    path(
        "proposal/<int:pk>/<str:action>/",
        ProposalActionView.as_view(),
        name="proposal_action",
    ),
    path("dashboard/dev/", DeveloperDashboardView.as_view(), name="dev_dashboard"),
]
