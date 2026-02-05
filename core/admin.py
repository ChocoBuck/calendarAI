from django.contrib import admin

from core import models


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "scheduling_mode", "auto_schedule_mode", "activity_tracking_opt_in")


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "detail", "user")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type", "user")


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "status", "protected", "user")


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "due_date", "priority", "user")


@admin.register(models.Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("title", "cadence", "user")


@admin.register(models.Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ("scope", "status", "confidence", "user")


@admin.register(models.MemoryFact)
class MemoryFactAdmin(admin.ModelAdmin):
    list_display = ("summary", "status", "confidence", "user")


@admin.register(models.ExternalCalendar)
class ExternalCalendarAdmin(admin.ModelAdmin):
    list_display = ("provider", "calendar_id", "user", "last_synced_at")


@admin.register(models.OnboardingState)
class OnboardingStateAdmin(admin.ModelAdmin):
    list_display = ("user", "current_step", "category_seeded", "completed_at")


@admin.register(models.PreferenceDigest)
class PreferenceDigestAdmin(admin.ModelAdmin):
    list_display = ("user", "week_start", "status", "generated_at", "delivered_at")


@admin.register(models.AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "agent_type", "enabled", "updated_at")
