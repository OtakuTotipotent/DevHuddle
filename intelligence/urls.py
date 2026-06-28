from django.urls import path
from .views import (
    ProfileAnalyzerView,
    PostAnalyzerView,
    AIDashboardView,
    AIDeleteReportView,
)

urlpatterns = [
    path(
        "dashboard/",
        AIDashboardView.as_view(),
        name="ai_dashboard",
    ),
    path(
        "analyze/profile/<str:username>/",
        ProfileAnalyzerView.as_view(),
        name="ai_analyze_profile",
    ),
    path(
        "analyze/post/<int:pk>/",
        PostAnalyzerView.as_view(),
        name="ai_analyze_post",
    ),
    path(
        "delete/<int:pk>/",
        AIDeleteReportView.as_view(),
        name="ai_delete",
    ),
]
