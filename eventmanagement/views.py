from datetime import timezone
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from .models import Event, Guest


def event_dashboard(request, event_id):
    # Fetch the event based on the event_id
    event = get_object_or_404(Event, id=event_id)

    # Retrieve all guests associated with this event
    guests = Guest.objects.filter(event=event)

    # Pass the event and guest list to the template
    return render(request, "eventmanagement/event_dashboard.html", {
        "event": event,

        "guests": guests,  # Add the guest list here
    })
    
    
def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        description = request.POST.get('description')

        # Create a new event instance
        event_instance = Event.objects.create(
            name=name,
            event_date=date,
            location=location,
            description=description,
            user=request.user  # Associate the event with the logged-in user
        )
        
        messages.success(request, "Event created successfully.")
        return redirect(reverse('event_dashboard', args=[event_instance.id]))

    return render(request, 'eventmanagement/create_event.html')

def add_guest(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)

    if request.method == 'POST':
        name = request.POST['guest_name']
        email = request.POST['guest_email']

        # Create the guest in the database
        guest = Guest.objects.create(
            event=event,
            name=name,
            email=email,
            rsvp_token=uuid.uuid4()
        )

        # Display a success message indicating the guest was added
        messages.success(request, f"Guest '{name}' added successfully.")

        # Redirect to the event dashboard or another page as needed
        return redirect(reverse('event_dashboard', args=[event.id]))

    return render(request, 'eventmanagement/add_guest.html', {'event': event})


def guest_rsvp(request, token):
    guest = get_object_or_404(Guest, rsvp_token=token)

    if request.method == 'POST':
        status = request.POST['rsvp_status']
        guest.rsvp_status = status
        guest.save()
        messages.success(request, "RSVP status updated successfully.")
        return redirect('thank_you')  # Create a thank-you page or redirect as needed

    return render(request, 'eventmanagement/guest_rsvp.html', {'guest': guest})



# def event_countdown_view(request):
#     # Retrieve the next upcoming event
  

#     return render(request, "index.html", {
        
#     })