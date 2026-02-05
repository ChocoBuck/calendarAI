from django.conf import settings
from django.db import models


class SchedulingMode(models.TextChoices):
    CLOSE = "close", "Close"
    LOOSE = "loose", "Loose"


class AutoScheduleMode(models.TextChoices):
    OFF = "off", "Off"
    SUGGEST = "suggest", "Suggest"
    AUTO = "auto", "Auto"


class CategoryType(models.TextChoices):
    EVENT = "event", "Event"
    TASK = "task", "Task"
    HABIT = "habit", "Habit"


class EventStatus(models.TextChoices):
    CONFIRMED = "confirmed", "Confirmed"
    PENDING = "pending", "Pending"


class EventSource(models.TextChoices):
    MANUAL = "manual", "Manual"
    AI = "ai", "AI"
    GOOGLE = "google", "Google"


class PreferenceScope(models.TextChoices):
    GLOBAL = "global", "Global"
    CATEGORY = "category", "Category"


class PreferenceStatus(models.TextChoices):
    SUGGESTED = "suggested", "Suggested"
    CONFIRMED = "confirmed", "Confirmed"
    REJECTED = "rejected", "Rejected"


class MemorySource(models.TextChoices):
    INFERRED = "inferred", "Inferred"
    CHAT = "chat", "Chat"
    USER = "user", "User"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=64, default="UTC")
    scheduling_mode = models.CharField(
        max_length=16, choices=SchedulingMode.choices, default=SchedulingMode.LOOSE
    )
    activity_tracking_opt_in = models.BooleanField(default=False)
    auto_schedule_mode = models.CharField(
        max_length=16, choices=AutoScheduleMode.choices, default=AutoScheduleMode.SUGGEST
    )
    confirm_delay_seconds = models.PositiveIntegerField(default=60)
    google_sync_delay_seconds = models.PositiveIntegerField(default=60)
    preference_confidence_threshold = models.FloatField(default=0.75)
    inferred_profile = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"Profile for {self.user}"


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.detail})" if self.detail else self.name


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    category_type = models.CharField(max_length=16, choices=CategoryType.choices)
    default_duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    default_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    parent_category = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    auto_created = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=16, choices=EventSource.choices, default=EventSource.MANUAL)
    external_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=16, choices=EventStatus.choices, default=EventStatus.CONFIRMED)
    protected = models.BooleanField(default=False)
    last_modified_by = models.CharField(max_length=16, choices=EventSource.choices, default=EventSource.MANUAL)
    pending_confirmation_until = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    vague_window = models.CharField(max_length=40, blank=True)
    duration_estimate_minutes = models.PositiveIntegerField(null=True, blank=True)
    priority = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    parent_task = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cadence = models.CharField(max_length=20)
    suggested_time = models.TimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Preference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scope = models.CharField(max_length=16, choices=PreferenceScope.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.JSONField(default=dict)
    confidence = models.FloatField(default=0.0)
    status = models.CharField(max_length=16, choices=PreferenceStatus.choices, default=PreferenceStatus.SUGGESTED)
    source = models.CharField(max_length=16, choices=MemorySource.choices, default=MemorySource.INFERRED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.scope} preference ({self.status})"


class MemoryFact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    summary = models.CharField(max_length=255)
    details = models.JSONField(default=dict, blank=True)
    confidence = models.FloatField(default=0.0)
    status = models.CharField(max_length=16, choices=PreferenceStatus.choices, default=PreferenceStatus.SUGGESTED)
    source = models.CharField(max_length=16, choices=MemorySource.choices, default=MemorySource.INFERRED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.summary


class ExternalCalendar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=40, default="google")
    calendar_id = models.CharField(max_length=200)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    sync_token = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return f"{self.provider}: {self.calendar_id}"
