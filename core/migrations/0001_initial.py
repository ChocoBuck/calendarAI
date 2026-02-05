# Generated manually for initial schema
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AgentProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("agent_type", models.CharField(choices=[("general", "General"), ("scheduler", "Scheduler"), ("task", "Task"), ("memory", "Memory")], max_length=16)),
                ("system_prompt", models.TextField()),
                ("enabled", models.BooleanField(default=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ExternalCalendar",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider", models.CharField(default="google", max_length=40)),
                ("calendar_id", models.CharField(max_length=200)),
                ("last_synced_at", models.DateTimeField(blank=True, null=True)),
                ("sync_token", models.CharField(blank=True, max_length=200)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("detail", models.CharField(blank=True, max_length=200)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="OnboardingState",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("current_step", models.CharField(default="scheduling_mode", max_length=64)),
                ("category_seeded", models.BooleanField(default=False)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("timezone", models.CharField(default="UTC", max_length=64)),
                ("scheduling_mode", models.CharField(choices=[("close", "Close"), ("loose", "Loose")], default="loose", max_length=16)),
                ("activity_tracking_opt_in", models.BooleanField(default=False)),
                ("auto_schedule_mode", models.CharField(choices=[("off", "Off"), ("suggest", "Suggest"), ("auto", "Auto")], default="suggest", max_length=16)),
                ("confirm_delay_seconds", models.PositiveIntegerField(default=60)),
                ("google_sync_delay_seconds", models.PositiveIntegerField(default=60)),
                ("preference_confidence_threshold", models.FloatField(default=0.75)),
                ("inferred_profile", models.JSONField(blank=True, default=dict)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("category_type", models.CharField(choices=[("event", "Event"), ("task", "Task"), ("habit", "Habit")], max_length=16)),
                ("default_duration_minutes", models.PositiveIntegerField(blank=True, null=True)),
                ("auto_created", models.BooleanField(default=False)),
                ("default_location", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.location")),
                ("parent_category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.category")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("duration_minutes", models.PositiveIntegerField(blank=True, null=True)),
                ("source", models.CharField(choices=[("manual", "Manual"), ("ai", "AI"), ("google", "Google")], default="manual", max_length=16)),
                ("external_id", models.CharField(blank=True, max_length=200)),
                ("status", models.CharField(choices=[("confirmed", "Confirmed"), ("pending", "Pending")], default="confirmed", max_length=16)),
                ("protected", models.BooleanField(default=False)),
                ("last_modified_by", models.CharField(choices=[("manual", "Manual"), ("ai", "AI"), ("google", "Google")], default="manual", max_length=16)),
                ("pending_confirmation_until", models.DateTimeField(blank=True, null=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.category")),
                ("location", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.location")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Habit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("cadence", models.CharField(max_length=20)),
                ("suggested_time", models.TimeField(blank=True, null=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.category")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="MemoryFact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("summary", models.CharField(max_length=255)),
                ("details", models.JSONField(blank=True, default=dict)),
                ("confidence", models.FloatField(default=0.0)),
                ("status", models.CharField(choices=[("suggested", "Suggested"), ("confirmed", "Confirmed"), ("rejected", "Rejected")], default="suggested", max_length=16)),
                ("source", models.CharField(choices=[("inferred", "Inferred"), ("chat", "Chat"), ("user", "User")], default="inferred", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Preference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("scope", models.CharField(choices=[("global", "Global"), ("category", "Category")], max_length=16)),
                ("value", models.JSONField(default=dict)),
                ("confidence", models.FloatField(default=0.0)),
                ("status", models.CharField(choices=[("suggested", "Suggested"), ("confirmed", "Confirmed"), ("rejected", "Rejected")], default="suggested", max_length=16)),
                ("source", models.CharField(choices=[("inferred", "Inferred"), ("chat", "Chat"), ("user", "User")], default="inferred", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.category")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="PreferenceDigest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("week_start", models.DateField()),
                ("status", models.CharField(choices=[("draft", "Draft"), ("delivered", "Delivered"), ("archived", "Archived")], default="draft", max_length=16)),
                ("items", models.JSONField(default=list)),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                ("delivered_at", models.DateTimeField(blank=True, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("due_date", models.DateTimeField(blank=True, null=True)),
                ("vague_window", models.CharField(blank=True, max_length=40)),
                ("duration_estimate_minutes", models.PositiveIntegerField(blank=True, null=True)),
                ("priority", models.PositiveIntegerField(default=0)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.category")),
                ("parent_task", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.task")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
