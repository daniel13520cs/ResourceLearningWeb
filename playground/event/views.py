# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Event, UserEvents
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages  # Import messages
from mongoengine.queryset.visitor import Q
from django.contrib.auth.models import User
from event.models import Event
from django.contrib import messages
from collections import Counter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Function to add a new event
@login_required
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        startTime = request.POST.get('startTime')
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

@login_required
def list_events(request):
    userEvents = UserEvents.objects.filter(userID=request.user.id)
    event_ids = [user_events.eventID for user_events in userEvents]
    events = Event.objects.filter(id__in=event_ids)

    event_list = []  # This will store new instances with the additional field
    for event in events:
        try:
            owner_user = User.objects.get(id=event.ownerUserID)
            owner_username = owner_user.username
        except User.DoesNotExist:
            owner_username = "Unknown"
        
        event_data = {
            'pk': event.id,
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'startTime': event.startTime,
            'URL': event.URL,
            'ownerUserID': event.ownerUserID,
            'ownerUsername': owner_username,
            'image': event.image,
        }
        event_list.append(event_data)

    # Paginate the event list
    paginator = Paginator(event_list, 5)  # Show 5 events per page
    page = request.GET.get('page', 1)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'events/list_events.html', {'events': events})

def list_publicEvents(request):
    publicEvents = Event.objects.filter(isPublic=True)
    
    event_list = []  # This will store new instances with the additional field
    for event in publicEvents:
        try:
            owner_user = User.objects.get(id=event.ownerUserID)
            owner_username = owner_user.username
        except User.DoesNotExist:
            owner_username = "Unknown"
        
        event_data = {
            'pk': event.id,
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'startTime': event.startTime,
            'URL': event.URL,
            'ownerUserID': event.ownerUserID,
            'ownerUsername': owner_username,
            'image': event.image,
        }
        event_list.append(event_data)

    # Paginate the event list
    paginator = Paginator(event_list, 5)  # Show 5 events per page
    page = request.GET.get('page', 1)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    topKEvent = GetTopKRecommendationEvents(request, publicEvents)

    return render(request, 'events/list_public_events.html', {'events': events, 'recommendedEvents': topKEvent})
@login_required
def optIn_publicEvents(request, event_id):
    if request.method == 'POST':
        # Check if the user has already opted into this event
        existing_user_event = UserEvents.objects.filter(userID=request.user, eventID=str(event_id)).first()
        
        if existing_user_event:
            messages.warning(request, 'You have already opted into this event.')
        else:
            # Create a new UserEvent if it doesn't exist
            user_event = UserEvents(
                userID=request.user,
                eventID=str(event_id)
            )
            user_event.save()  # Save the new UserEvent record
            messages.success(request, 'You have successfully opted into the event!')
    
    return redirect('list_publicEvents')  # Redirect to the event list

@login_required
def optOut_publicEvents(request, event_id):
    if request.method == 'POST':
        # Check if the user has already opted into this event
        existing_user_event = UserEvents.objects.filter(userID=request.user, eventID=str(event_id)).first()
        
        if existing_user_event:
            # If the event exists, delete the user's opt-in record
            existing_user_event.delete()
            messages.success(request, 'You have successfully opted out of the event.')
        else:
            messages.warning(request, 'You have not opted into this event yet.')
    
    return redirect('list_events')  # Redirect to the event list

@login_required
def optOut_allOptedInEvents(request):
    if request.method == 'POST':
        # Retrieve all events the user has opted into
        user_events = UserEvents.objects.filter(userID=request.user)

        if user_events.exists():
            # Delete all user's opt-in records
            user_events.delete()
            messages.success(request, 'You have successfully opted out of all events.')
        else:
            messages.warning(request, 'You have not opted into any events.')

    return redirect('list_events')  # Redirect to the event list



# Function to delete an event
@login_required
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        userEvent = UserEvents.objects.get(eventID=event_id, userID=request.user.id)  # Check for user ownership
    except Event.DoesNotExist:
        raise Http404("Event not found")
    
    if request.method == 'POST':
        if request.user.id == event.ownerUserID:
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
    
def GetTopKRecommendationEvents(request, publicEvents, K=5):
    if not request.user.is_authenticated:
        return []
    # Fetch the events the user has opted into
    user_events = UserEvents.objects.filter(userID=request.user)

    if not user_events.exists():
        messages.warning(request, 'You have not opted into any events.')
        return []

    # Extract the event IDs and fetch the events
    opted_in_event_ids = [ue.eventID for ue in user_events]
    opted_in_events = Event.objects.filter(id__in=opted_in_event_ids)

    # Get all tags from the user's opted-in events
    user_tags = []
    for event in opted_in_events:
        user_tags.extend(event.tags)  # Assuming `tags` is a list field in your Event model
    
    # Count the frequency of each tag
    tag_counter = Counter(user_tags)
  
    # Fetch public events that the user has not opted into
    public_events = publicEvents.filter(Q(id__nin=opted_in_event_ids))  # Use `__nin` for "not in"

    # Rank the public events based on matching tags
    event_rankings = []
    for event in public_events:
        # Count matching tags between the user's tags and the event's tags
        matching_tags = set(event.tags).intersection(tag_counter.keys())
        rank_score = sum(tag_counter[tag] for tag in matching_tags)  # Score based on tag frequency
        event_rankings.append((event, rank_score))
    
    # Sort events by rank score in descending order
    event_rankings.sort(key=lambda x: x[1], reverse=True)

    # Get the top K recommended events
    top_k_events = [event for event, score in event_rankings[:K]]

    # Create a JSON response with event details
    response_data = [
        {
            'pk': event.id,
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "startTime": event.startTime,
            "URL": event.URL,
            "tags": event.tags,
            "ownerUsername": User.objects.get(id=event.ownerUserID).username,
            "image": event.image,
        } 
        for event in top_k_events
    ]
    
    return response_data    

@login_required
@user_passes_test(lambda user: user.is_superuser)
def retag_all_events(request):
    # if request.method == 'POST':
    #     knn_strategy = KNNStrategy(n_neighbors=3)
    #     tagger = EventTagger(clustering_strategy=knn_strategy)
    #     tagger.autotag_public_events()
    # messages.success(request, "All tags have been classified from all events.")
    return redirect('manage')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def clear_all_event_tags(request):
    if request.method == 'POST':
        # # Fetch all public events from the database
        # events = Event.objects.filter(isPublic=True)

        # # Check if events are actually being fetched
        # if not events:
        #     messages.error(request, "No public events found to clear tags from.")
        #     return redirect('manage')
        
        # # Clear tags for each event
        # for event in events:
        #     event.tags = []  # Clear all tags
        #     event.save()  # Ensure the event is saved after clearing

        # # Add success message after tags are cleared
        # messages.success(request, "All public events tags have been cleared.")

        return redirect('manage')