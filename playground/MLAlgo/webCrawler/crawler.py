import requests
from datetime import datetime, timezone
from mongoengine import connect, Document, StringField, DateTimeField, URLField, IntField, BooleanField, ListField
import urllib.parse

# MongoDB Connection
username = 'daniel13520cs'
password = 'nlmIVD8svGikrjtG'

# Escape the username and password for the connection URI
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)
connection_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@playground.lskld.mongodb.net/Playground?retryWrites=true&w=majority"

# Try connecting to MongoDB
try:
    connect(host=connection_uri)
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Event model definition with length restrictions
class Event(Document):
    title = StringField(required=True, max_length=100)
    description = StringField(required=True)
    startTime = DateTimeField(required=True, default=datetime.utcnow)
    location = StringField(default='', blank=True, null=True, max_length=255)
    URL = URLField(blank=True, null=True)  # Allow this field to be empty
    ownerUserID = IntField(required=True)
    isPublic = BooleanField(default=False)
    tags = ListField(StringField(), default=[])
    image = StringField(blank=True, null=True, max_length=200)  # Restrict length to 200 chars
    venue = StringField(blank=True, null=True, max_length=200)  # Restrict length to 200 chars

    def __str__(self):
        return self.title

# Function to fetch events from Wikipedia API
def crawl_events(topic='2024 in science'):
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": topic,
        "utf8": 1,
        "srlimit": 10  # Limit to 10 results
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Failed to retrieve events: {response.status_code}, Response: {response.text}")
        return []

    data = response.json()
    events = []

    # Extract events from the response
    if 'query' in data and 'search' in data['query']:
        for item in data['query']['search']:
            try:
                title = item['title'][:200]  # Limit title to 200 chars
                page_id = item['pageid']

                # Fetch additional details for the event
                details_params = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts|pageimages",
                    "pageids": page_id,
                    "explaintext": True,
                    "exlimit": 1
                }

                details_response = requests.get(url, params=details_params)
                details_data = details_response.json()

                # Truncate strings to their maximum lengths
                description = details_data['query']['pages'][str(page_id)]['extract'][:200]  # Limit description to 200 chars
                image_url = details_data['query']['pages'][str(page_id)].get('thumbnail', {}).get('source', None)
                image_url = image_url[:200] if image_url else None  # Limit image URL to 200 chars
                event_url = f"https://en.wikipedia.org/?curid={page_id}"

                # Example start time; you can modify this to extract actual dates if available
                start_time = datetime.now(timezone.utc)

                event = Event(
                    title=title,
                    description=description,
                    startTime=start_time,
                    location="Unknown",  # Modify as needed
                    URL=event_url,
                    ownerUserID=2,
                    isPublic=True,
                    image=image_url,
                    venue="Wikipedia"  # Assuming Wikipedia as the venue
                )
                events.append(event)
            except Exception as e:
                print(f"Failed to parse event: {e}")
    
    return events

# Function to store events in MongoDB
def store_events(events):
    for event in events:
        try:
            existing_event = Event.objects(title=event.title, startTime=event.startTime).first()
            if not existing_event:
                event.save()
                print(f"Saved event: {event.title}")
            else:
                print(f"Event already exists: {event.title}")
        except Exception as e:
            print(f"Error saving event {event.title}: {e}")

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
    events = crawl_events()
    
    if not events:
        print("No events found.")
        return
    
    print_events(events)
    
    user_input = input("Do you want to store these events in the database? (Y/N): ").strip().upper()
    
    if user_input == 'Y':
        store_events(events)
    else:
        print("Events not stored in the database.")

if __name__ == "__main__":
    crawl_and_store()
