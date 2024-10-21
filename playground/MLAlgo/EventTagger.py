from sentence_transformers import SentenceTransformer
import ClusteringStrategy
from webCrawler.crawler import Event
import numpy as np

class EventTagger:
    def __init__(self, clustering_strategy: ClusteringStrategy):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.clustering_strategy = clustering_strategy

    def autotag_public_events(self):
        # Fetch all public events from the database
        events = Event.objects(isPublic=True)
        
        # Combine title and description into one text for each event
        event_texts = [f"{event.title}: {event.description}" for event in events]
        
        # Generate embeddings for each event's combined text
        embeddings = self.model.encode(event_texts)
        
        # Apply the chosen clustering algorithm
        knn_model = self.clustering_strategy.fit(embeddings)
        
        # Find neighbors and assign tags
        for i, event in enumerate(events):
            neighbors = knn_model.kneighbors(embeddings[i].reshape(1, -1), return_distance=False)
            neighbor_labels = [f"Cluster-{j}" for j in neighbors[0]]  # Generate cluster-like tags based on neighbors
            
            # Use a set to avoid duplicate tags
            for label in neighbor_labels:
                if label not in event.tags:
                    event.tags.append(label)
                    event.save()
            
            # Print the event's title and the assigned tags
            print(f"Event '{event.title}' has been tagged with: {', '.join(neighbor_labels)}")

    def autotag_single_event(self, event_id):
        # Fetch the event by ID from MongoDB
        event = Event.objects(id=event_id).first()
        
        if not event:
            print(f"Event with ID {event_id} not found.")
            return
        
        # Combine title and description into one text for the event
        event_text = f"{event.title}: {event.description}"
        
        # Generate the embedding for the single event's combined text
        event_embedding = self.model.encode([event_text])
        
        # Fetch all previously tagged events (to cluster this new one with existing ones)
        all_events = Event.objects(id__ne=event_id)  # Exclude the current event
        
        if not all_events:
            print("No previous events to compare with.")
            return
        
        # Combine existing event embeddings with the new event embedding
        previous_texts = [f"{e.title}: {e.description}" for e in all_events]
        previous_embeddings = self.model.encode(previous_texts)
        
        # Stack the new event's embedding with the previous ones
        all_embeddings = np.vstack([previous_embeddings, event_embedding])
        
        # Apply the chosen clustering algorithm on all embeddings (including the new one)
        knn_model = self.clustering_strategy.fit(all_embeddings)
        
        # Find the nearest neighbors for the new event
        neighbors = knn_model.kneighbors(event_embedding.reshape(1, -1), return_distance=False)
        
        # Assign cluster-like tags based on neighbors
        new_event_labels = [f"Cluster-{j}" for j in neighbors[0]]
        
        # Update the event's tags field in MongoDB (if not already tagged)
        for label in new_event_labels:
            if label not in event.tags:
                event.tags.append(label)
                event.save()
        
        # Print the event's title and the assigned tags
        print(f"Event '{event.title}' has been tagged with: {', '.join(new_event_labels)}")

    def recommend_non_opted_in_public_events(self, user_id):
        # Fetch the user's opted-in events
        opted_in_events = Event.objects(ownerUserID=user_id)
        
        if not opted_in_events:
            print("No opted-in events found for this user.")
            return []

        # Gather tags from opted-in events
        opted_in_tags = set()
        for event in opted_in_events:
            opted_in_tags.update(event.tags)

        # Fetch all public events excluding those the user has opted into
        public_events = Event.objects(isPublic=True, id__nin=[event.id for event in opted_in_events])
        
        # Recommend events that share tags with opted-in events
        recommended_events = []
        for event in public_events:
            if set(event.tags) & opted_in_tags:  # Check for shared tags
                recommended_events.append(event)

        # Print recommended events' titles and tags
        for event in recommended_events:
            print(f"Recommended Event: '{event.title}' with tags: {', '.join(event.tags)}")

        return recommended_events

# Main execution
if __name__ == "__main__":
    # Instantiate the EventTagger with your clustering strategy
    clustering_strategy = ClusteringStrategy.KNNStrategy()  # Replace with actual strategy implementation
    event_tagger = EventTagger(clustering_strategy)

    # Call the autotag_public_events method to auto-tag the public events
    event_tagger.autotag_public_events()
