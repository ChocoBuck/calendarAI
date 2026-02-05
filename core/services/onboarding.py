from dataclasses import dataclass

from django.contrib.auth import get_user_model

from core.models import Category, CategoryType, OnboardingState

User = get_user_model()


@dataclass(frozen=True)
class CategorySeed:
    name: str
    category_type: str


DEFAULT_CATEGORY_SEEDS = [
    CategorySeed(name="Work", category_type=CategoryType.EVENT),
    CategorySeed(name="Study", category_type=CategoryType.EVENT),
    CategorySeed(name="Exercise", category_type=CategoryType.EVENT),
    CategorySeed(name="Meals", category_type=CategoryType.EVENT),
    CategorySeed(name="Chores", category_type=CategoryType.EVENT),
    CategorySeed(name="Assignments", category_type=CategoryType.TASK),
    CategorySeed(name="Habits", category_type=CategoryType.HABIT),
]


def seed_default_categories(user: User) -> int:
    created_count = 0
    for seed in DEFAULT_CATEGORY_SEEDS:
        _, created = Category.objects.get_or_create(
            user=user,
            name=seed.name,
            defaults={"category_type": seed.category_type, "auto_created": True},
        )
        if created:
            created_count += 1
    OnboardingState.objects.update_or_create(
        user=user, defaults={"category_seeded": True, "current_step": "categories"}
    )
    return created_count
