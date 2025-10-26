from .models import Event


def user_event(request):
    if request.user.is_authenticated:
        event = Event.objects.filter(user=request.user).order_by('-event_date').first()
        return {'current_event': event}
    return {}
