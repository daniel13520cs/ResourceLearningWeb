# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Event, UserEvents
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages
from mongoengine.queryset.visitor import Q


# Function to add a new event
@login_required
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
            URL=URL or None,
            ownerUserID = request.user.id
        )
        event.save()
        userEvents = UserEvents(
            userID = request.user, #foreign key
            eventID = str(event.pk)
        )
        userEvents.save()
        return redirect('list_events')  # Redirect to the event list
    return render(request, 'events/add_event.html')  # Render the form template

# Function to list all events
@login_required
def list_events(request):
    userEvents = UserEvents.objects.filter(userID = request.user.id)
    event_ids = [user_events.eventID for user_events in userEvents]
    events = Event.objects.filter(id__in = event_ids)
    return render(request, 'events/list_events.html', {'events': events})  # Render the template with events

def list_publicEvents(request):
    publicEvents = Event.objects.filter(isPublic = True)
    return render(request, 'events/list_public_events.html', {'events': publicEvents})  # Render the template with events

def optIn_publicEvents(request, event_id): 
    userEvent = UserEvents(
        userID = request.user,
        eventID = str(event_id)
    )
    return redirect('list_publicEvents')  # Redirect to the event list


# Function to delete an event
@login_required
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        userEvent = UserEvents.objects.get(eventID=event_id, userID=request.user.id)  # Check for user ownership
    except Event.DoesNotExist:
        raise Http404("Event not found")
    
    if request.method == 'POST':
        if str(request.user.id) == event.ownerUserID:
            event.delete()
        userEvent.delete()
        return redirect('list_events')  # Redirect to the event list

    return render(request, 'events/delete_event.html', {'event': event})  # Render confirmation page

# Function to update an event
@login_required
def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event not found")

    if request.user.id != event.ownerUserID:
        messages.error(request, "You are not authorized to update this event.")  # Add an error message
        return redirect('list_events')  # Redirect to the event list        

    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)  # Update title
        event.description = request.POST.get('description', event.description)  # Update description
        event.startTime = datetime.fromisoformat(request.POST.get('startTime', event.startTime))  # Update start time
        event.location = request.POST.get('location', event.location)  # Update location
        event.URL = request.POST.get('URL', event.URL)  # Update URL
        event.save()  # Save the updated event
        return redirect('list_events')  # Redirect to the event list
    return render(request, 'events/update_event.html', {'event': event})  # Render the form for updating

@login_required
def publish_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event not found")
    
    if request.method == 'POST':
        if event.isPublic == True:
            messages.warning(request, 'This event was published')
        else:
            event.isPublic = True
            event.save()
            messages.success(request, 'The event is successfully published!')
    return redirect('list_events')
    