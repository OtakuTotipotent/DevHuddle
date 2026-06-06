from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill, Project, Experience

# Standard User Admin
admin.site.register(CustomUser, UserAdmin)


# New Normalized Models
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "user__username")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "user", "start_date", "is_current")
    list_filter = ("is_current", "start_date")
    search_fields = ("role", "company", "user__username")
