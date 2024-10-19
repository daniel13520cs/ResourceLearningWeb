from sklearn.neighbors import NearestNeighbors

class ClusteringStrategy:
    def fit(self, embeddings):
        raise NotImplementedError
    
class KNNStrategy(ClusteringStrategy):
    def __init__(self, n_neighbors=3):
        self.n_neighbors = n_neighbors

    def fit(self, embeddings):
        knn = NearestNeighbors(n_neighbors=self.n_neighbors, metric='cosine')
        knn.fit(embeddings)
        return knn
