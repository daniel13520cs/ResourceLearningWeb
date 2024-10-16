# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Event
from datetime import datetime
# Function to add a new event
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        startTime = request.POST.get('startTime')
        location = request.POST.get('location')
        URL = request.POST.get('URL')
        
        # Convert the start time string to a datetime object
        try:
            startTime = datetime.fromisoformat(startTime)  # Convert the ISO format string to a datetime object
        except ValueError:
            # Handle invalid date format error
            return render(request, 'events/add_event.html', {'error': 'Invalid date format.'})
        
        # Create and save the new Event
        event = Event(
            title=title,
            description=description,
            startTime=startTime,
            location=location,
            URL=URL or None
        )
        event.save()
        return redirect('list_events')  # Redirect to the event list
    return render(request, 'events/add_event.html')  # Render the form template

# Function to list all events
def list_events(request):
    events = Event.objects.all()  # Retrieve all events from the database
    return render(request, 'events/list_events.html', {'events': events})  # Render the template with events

# Function to delete an event
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event not found")
    
    if request.method == 'POST':
        event.delete()  # Delete the event
        return redirect('list_events')  # Redirect to the event list

    return render(request, 'events/delete_event.html', {'event': event})  # Render confirmation page

# Function to update an event
def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event not found")

    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)  # Update title
        event.description = request.POST.get('description', event.description)  # Update description
        event.startTime = datetime.fromisoformat(request.POST.get('startTime', event.startTime))  # Update start time
        event.location = request.POST.get('location', event.location)  # Update location
        event.URL = request.POST.get('URL', event.URL)  # Update URL
        event.save()  # Save the updated event
        return redirect('list_events')  # Redirect to the event list
    return render(request, 'events/update_event.html', {'event': event})  # Render the form for updating
