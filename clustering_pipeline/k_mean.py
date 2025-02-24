import os
import sys
import numpy as np
import pandas as pd
import json
import umap
from typing import Tuple, List
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class ClusteringConfig:
    min_clusters: int = 3  # Changed to 2
    max_clusters: int = 15
    random_state: int = 42
    umap_n_components: int = 2
    umap_n_neighbors: int = 50
    umap_min_dist: float = 0.02

class Cluster:
    def __init__(self, config: ClusteringConfig = ClusteringConfig()):
        self.config = config
        self.embedder = SentenceTransformer('all-mpnet-base-v2')

    def kmeans_clustering(self, n_clusters: int, embeddings: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

        model = KMeans(
            n_clusters=n_clusters,
            init='k-means++',
            random_state=self.config.random_state,
            n_init=10
        )
        model.fit(embeddings)
        return model.labels_, model.cluster_centers_

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.embedder.encode(texts)

    def reduce_dimensions(self, embeddings: np.ndarray) -> np.ndarray:

        reducer = umap.UMAP(
            n_components=self.config.umap_n_components,
            n_neighbors=self.config.umap_n_neighbors,
            min_dist=self.config.umap_min_dist,
            random_state=self.config.random_state
        )
        return reducer.fit_transform(embeddings)

    def find_optimal_clusters(self, embeddings: np.ndarray) -> int:

        n_samples = embeddings.shape[0]
        
        # Adjust max_clusters based on sample size
        max_clusters = min(self.config.max_clusters, n_samples - 1)
        min_clusters = min(self.config.min_clusters, max_clusters - 1)
        
        if max_clusters <= min_clusters:
            return min_clusters
            
        inertias = []
        
        for n_clusters in range(min_clusters, max_clusters + 1):
            kmeans = KMeans(
                n_clusters=n_clusters,
                init='k-means++',
                random_state=self.config.random_state,
                n_init=10
            )
            kmeans.fit(embeddings)
            inertias.append(kmeans.inertia_)

        # Find elbow point using the percentage of variance explained
        inertias = np.array(inertias)
        diffs = np.diff(inertias)
        diffs_r = diffs[1:] / diffs[:-1]
        
        if len(diffs_r) > 0:
            elbow_point = np.argmin(diffs_r) + min_clusters + 1
        else:
            elbow_point = min_clusters

        return min(elbow_point, max_clusters)

    def find_optimal_clusters_silhouette(self, embeddings: np.ndarray) -> int:
        n_samples = embeddings.shape[0]

        # Adjust max_clusters based on sample size
        max_clusters = min(self.config.max_clusters, n_samples - 1)
        min_clusters = min(self.config.min_clusters, max_clusters - 1)

        if max_clusters <= min_clusters:
            return min_clusters

        best_n_clusters = min_clusters
        best_silhouette = -1
        silhouette_scores = []

        cluster_range = range(min_clusters, max_clusters + 1)

        for n_clusters in cluster_range:
            kmeans = KMeans(
                n_clusters=n_clusters,
                init="k-means++",
                random_state=self.config.random_state,
                n_init=10
            )
            cluster_labels = kmeans.fit_predict(embeddings)
            silhouette_avg = silhouette_score(embeddings, cluster_labels)

            silhouette_scores.append(silhouette_avg)

            if silhouette_avg > best_silhouette:
                best_silhouette = silhouette_avg
                best_n_clusters = n_clusters

        # Plot the silhouette scores
        # plt.figure(figsize=(8, 5))
        # plt.plot(cluster_range, silhouette_scores, marker='o', linestyle='-')
        # plt.xlabel("Number of Clusters")
        # plt.ylabel("Silhouette Score")
        # plt.title("Silhouette Score vs. Number of Clusters")
        # plt.grid(True)
        # plt.show()
        print(silhouette_scores)
        return best_n_clusters
    
    
    

    def process_clustering(self, data_path: str, metadata_column: str) -> dict:

        try:
            # Load and validate data
            # with open(data_path, 'r', encoding='utf-8') as json_file:
            #     data = json.load(json_file)
                
            if not isinstance(data_path, list):
                raise ValueError("Input data must be a list of records")
            # data = data[data]
            # print("hello")
            # print(data)
            df = pd.DataFrame(data_path)
            # df = pd.read_csv(data_path)
            if metadata_column not in df.columns:
                raise ValueError(f"Column '{metadata_column}' not found in data")

            # Process clustering
            # texts = df["keywords"].values
            embeddings = self.embed_texts(df[metadata_column].values)
            reduced_embeddings = self.reduce_dimensions(embeddings)
            
            # Validate sample size
            n_samples = len(df)
            if n_samples < 10:
                raise ValueError("Need at least 40 keywords for clustering")

            optimal_clusters = self.find_optimal_clusters_silhouette(reduced_embeddings)
            print(f"Optimal cluster: {optimal_clusters}")
            labels, centers = self.kmeans_clustering(optimal_clusters, reduced_embeddings)
            print(centers)
            # Create visualization
            # self.plot_clusters(reduced_embeddings, labels, centers)
            # self.plot_clusters_with_text(reduced_embeddings, labels, centers, texts)

            # Add cluster labels and coordinates to DataFrame
            df['cluster'] = labels
            # df.to_csv(r"C:\Users\nickc\OneDrive\Desktop\SEO\clustering_pipeline\cluster_data\clusterdata.csv", index=False)
            # df['x_coordinate'] = reduced_embeddings[:, 0]
            # df['y_coordinate'] = reduced_embeddings[:, 1]
            
            # # Add center coordinates for each point
            # df['center_x'] = df['cluster'].map({i: centers[i][0] for i in range(len(centers))})
            # df['center_y'] = df['cluster'].map({i: centers[i][1] for i in range(len(centers))})
            # Prepare results
            results = {
                'optimal_clusters': optimal_clusters,
                'cluster_labels': labels.tolist(),
                'cluster_centers': centers.tolist(),
                'reduced_embeddings': reduced_embeddings.tolist()
            }

            print(results)
            
            json_string = df.to_json(orient='records', lines=False)
            return json_string , optimal_clusters

        except Exception as e:
            raise Exception(f"Clustering pipeline failed: {str(e)}") from e

# if __name__ == "__main__":
    # config = ClusteringConfig(
    #     min_clusters=4,  
    #     max_clusters=20,
    #     random_state=42
    # )
    
    # clusterer = Cluster(config)
    # metadata_column = "Keyword"
    # data_path = r"C:\Users\nickc\OneDrive\Desktop\SEO\data\input test 2 - input test 2.csv"

    # try:
    #     results = clusterer.process_clustering(data_path, metadata_column)
    #     print(results)
    #     # print(f"Optimal number of clusters: {results['optimal_clusters']}")
    #     # print(f"Number of documents processed: {len(results['cluster_labels'])}")
    # except Exception as e:
    #     print(f"Error: {str(e)}")