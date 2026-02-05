import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from core.models import Category, Event, OnboardingState


@require_GET
def health_check(_request):
    return JsonResponse({"status": "ok"})


@require_GET
def onboarding_status(request: HttpRequest):
    state, _ = OnboardingState.objects.get_or_create(user=request.user)
    return JsonResponse(
        {
            "current_step": state.current_step,
            "category_seeded": state.category_seeded,
            "completed_at": state.completed_at,
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def categories(request: HttpRequest):
    if request.method == "GET":
        category_list = [
            {"id": category.id, "name": category.name, "type": category.category_type}
            for category in Category.objects.filter(user=request.user).order_by("name")
        ]
        return JsonResponse({"categories": category_list})

    payload = json.loads(request.body or "{}")
    category = Category.objects.create(
        user=request.user,
        name=payload.get("name", "Untitled"),
        category_type=payload.get("type", "event"),
        auto_created=False,
    )
    return JsonResponse({"id": category.id, "name": category.name, "type": category.category_type})


@csrf_exempt
@require_http_methods(["POST"])
def create_event(request: HttpRequest):
    payload = json.loads(request.body or "{}")
    event = Event.objects.create(
        user=request.user,
        title=payload.get("title", "Untitled"),
        start_time=payload["start_time"],
        end_time=payload["end_time"],
        category_id=payload.get("category_id"),
        location_id=payload.get("location_id"),
    )
    return JsonResponse({"id": event.id, "title": event.title})
