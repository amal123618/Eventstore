from datetime import timezone
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Event, Guest
from django.core.exceptions import PermissionDenied

@login_required(login_url='login')   
def event_dashboard(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.user != request.user:
        raise PermissionDenied("You do not have permission to view this event.")

    guests = Guest.objects.filter(event=event)
    return render(request, "eventmanagement/event_dashboard.html", {
        "event": event,
        "guests": guests, 
    })
@login_required(login_url='login')   
def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        description = request.POST.get('description')
        event_instance = Event.objects.create(
            name=name,
            event_date=date,
            location=location,
            description=description,
            user=request.user  
        )
        
        messages.success(request, "Event created successfully.")
        return redirect(reverse('event_dashboard', args=[event_instance.id]))

    return render(request, 'eventmanagement/create_event.html')
@login_required(login_url='login')   
def add_guest(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)

    if request.method == 'POST':
        name = request.POST['guest_name']
        email = request.POST['guest_email']

    
        guest = Guest.objects.create(
            event=event,
            name=name,
            email=email,
            rsvp_token=uuid.uuid4()
        )
        messages.success(request, f"Guest '{name}' added successfully.")
        return redirect(reverse('event_dashboard', args=[event.id]))

    return render(request, 'eventmanagement/add_guest.html', {'event': event})

@login_required(login_url='login')   
def guest_rsvp(request, token):
    guest = get_object_or_404(Guest, rsvp_token=token)

    if request.method == 'POST':
        status = request.POST['rsvp_status']
        guest.rsvp_status = status
        guest.save()
        messages.success(request, "RSVP status updated successfully.")
        return redirect('thank_you') 

    return render(request, 'eventmanagement/guest_rsvp.html', {'guest': guest})



# def event_countdown_view(request):
#     # Retrieve the next upcoming event
  

#     return render(request, "index.html", {
        
#     })