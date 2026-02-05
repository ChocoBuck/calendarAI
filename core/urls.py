from django.urls import path

from core import views

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
    path("onboarding/status/", views.onboarding_status, name="onboarding_status"),
    path("categories/", views.categories, name="categories"),
    path("events/", views.create_event, name="create_event"),
]
