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
    description = StringField(required=True, max_length=400)  # Updated max_length to 400
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

# Function to fetch random book events from Google Books API
def crawl_books(num_events=10, api_key="AIzaSyBFAb0wlxYHdYRZfRF9urFww4Cjh5ZWu2o"):
    url = f"https://www.googleapis.com/books/v1/volumes"

    # Request random books
    params = {
        "q": "fiction",  # You can change the query as needed
        "maxResults": num_events,
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to retrieve books: {response.status_code}, Response: {response.text}")
        return []

    data = response.json()
    events = []

    # Extract books from the response
    for item in data.get('items', []):
        try:
            title = item['volumeInfo'].get('title', 'No title available')[:100]  # Limit title to 100 chars
            description = item['volumeInfo'].get('description', 'No description available.')[:400]  # Limit description to 400 chars
            image_url = item['volumeInfo'].get('imageLinks', {}).get('thumbnail', None)
            image_url = image_url[:200] if image_url else None  # Limit image URL to 200 chars
            event_url = item['volumeInfo'].get('infoLink', 'No URL available')

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
                venue="Google Books"  # Assuming Google Books as the venue
            )
            events.append(event)
        except Exception as e:
            print(f"Failed to parse book event: {e}")

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
    # Fetch random book events
    book_events = crawl_books(10)  # Fetch 10 random books
    # Fetch random Wikipedia events

    # Combine both lists of events
    events = book_events

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
