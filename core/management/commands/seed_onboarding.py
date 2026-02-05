from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from core.services.onboarding import seed_default_categories

User = get_user_model()


class Command(BaseCommand):
    help = "Seed default onboarding categories for a user."

    def add_arguments(self, parser) -> None:
        parser.add_argument("user_id", type=int, help="User ID to seed categories for")

    def handle(self, *args, **options) -> None:
        user_id = options["user_id"]
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise CommandError(f"User {user_id} does not exist") from exc

        created_count = seed_default_categories(user)
        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} categories."))
