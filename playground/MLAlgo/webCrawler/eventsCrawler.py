import requests
from datetime import datetime
from mongoengine import connect
from mongoengine import Document, StringField, DateTimeField, URLField, IntField, BooleanField, ListField
import urllib

# Same one defined in Django app for local ML models use
class Event(Document):
    title = StringField(required=True, max_length=100)
    description = StringField(required=True)
    startTime = DateTimeField(required=True, default=datetime.utcnow)
    location = StringField(default='', blank=True, null=True, max_length=255)
    URL = URLField(blank=True, null=True)  # Allow this field to be empty
    ownerUserID = IntField(required=True)
    isPublic = BooleanField(default=False)
    tags = ListField(StringField(), default=[])  # Field to store assigned tags
    image = StringField(blank=True, null=True)  # Additional field for event image
    venue = StringField(blank=True, null=True)  # Additional field for venue information

    def __str__(self):
        return self.title
    
username = 'daniel13520ccs'
password = 'nlmIVD8svGikrjtG'

# Escape the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)
connection_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@playground.lskld.mongodb.net/Playground?retryWrites=true&w=majority"
# Establish a connection to the MongoDB database
connect(host=connection_uri)

# Function to crawl and parse event data from Ticketmaster API
def crawl_events(url=None, maxEventsCrawled=10, adminUserID=2):
    if url is None or url == '':
        url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    
    # Your Ticketmaster API key
    api_key = 'TtkqqIHsE9TIHDocjdElkklVqx96WDN6'  # Replace with your actual API key

    # Parameters for the API request
    params = {
        'apikey': api_key,
        'city': 'Seattle',  # You can adjust this to filter events
        'size': maxEventsCrawled,  # Number of events to return
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve events: {response.status_code}")
        return []

    data = response.json()
    events = []

    # Extract events from the response
    if '_embedded' in data and 'events' in data['_embedded']:
        for event_data in data['_embedded']['events']:
            try:
                event_id = event_data['id']  # Get the event ID
                title = event_data['name']
                description = event_data.get('description', 'No description available')
                start_time_str = event_data['dates']['start']['localDate']
                start_time = datetime.fromisoformat(start_time_str)
                location = event_data['_embedded']['venues'][0]['name'] if '_embedded' in event_data else "Unknown"
                event_url = event_data['url']
                image = event_data['images'][0]['url'] if 'images' in event_data and event_data['images'] else None
                
                # Fetch additional event details
                details = get_event_details(event_id, api_key)
                
                event = Event(
                    title=title,
                    description=description,
                    startTime=start_time,
                    location=location,
                    URL=event_url,
                    ownerUserID=adminUserID,  # Assuming this is the admin or default user
                    isPublic=True,
                    image=image,
                    venue=details.get('venue', 'N/A')  # Store additional venue details if available
                )
                events.append(event)
            except Exception as e:
                print(f"Failed to parse event: {e}")
    
    return events

# Function to fetch detailed information for a specific event
def get_event_details(event_id, api_key):
    url = f'https://app.ticketmaster.com/discovery/v2/events/{event_id}.json'
    params = {
        'apikey': api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve details for event ID {event_id}: {response.status_code}")
        return {}

    return response.json()

# Function to store events in MongoDB
def store_events(events):
    for event in events:
        existing_event = Event.objects(title=event.title, startTime=event.startTime).first()
        if not existing_event:
            event.save()
            print(f"Saved event: {event.title}")
        else:
            print(f"Event already exists: {event.title}")

# Function to print events
def print_events(events):
    for i, event in enumerate(events, 1):
        print(f"Event {i}:")
        print(f"Title: {event.title}")
        print(f"Description: {event.description}")
        print(f"Start Time: {event.startTime}")
        print(f"Location: {event.location}")
        print(f"URL: {event.URL}")
        print(f"Image: {event.image}")
        print(f"Venue: {event.venue}")
        print("-" * 40)

# Main function to crawl, print, and conditionally store events
def crawl_and_store():
    website_input = input("Please provide the url to crawl events (leave blank for default):")
    
    events = crawl_events(url=website_input if website_input else None)
    
    if not events:
        print("No events found.")
        return
    
    # Print the events
    print_events(events)
    
    # Ask the user if they want to store the events in the database
    user_input = input("Do you want to store these events in the database? (Y/N): ").strip().upper()
    
    if user_input == 'Y':
        store_events(events)
    else:
        print("Events not stored in the database.")

crawl_and_store()
