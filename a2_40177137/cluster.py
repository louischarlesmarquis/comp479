import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict

# Constants for clustering
NUM_DEPARTMENTS = 5  
NUM_FACULTIES = 3  

# Load the positional index
def load_positional_index(filename="positional_index.json"):
    with open(filename, "r", encoding="utf-8") as f:
        positional_index = json.load(f)
    return positional_index

# Convert the positional index into a document-term matrix
def create_document_term_matrix(positional_index):
    documents = defaultdict(str)
    for term, postings in positional_index.items():
        for doc_id in postings:
            documents[doc_id] += f" {term}"
    doc_ids = list(documents.keys())
    doc_texts = list(documents.values())
    return doc_ids, doc_texts

# Perform clustering and extract top terms for each cluster
def cluster_documents(doc_ids, doc_texts, num_clusters, output_file):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(doc_texts)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)

    # Assign clusters
    clusters = defaultdict(list)
    for doc_id, label in zip(doc_ids, kmeans.labels_):
        clusters[label].append(doc_id)

    # Extract top terms for each cluster
    cluster_top_terms = {}
    for cluster_id in range(num_clusters):
        cluster_indices = [i for i, label in enumerate(kmeans.labels_) if label == cluster_id]
        cluster_matrix = X[cluster_indices]
        mean_tfidf = np.array(cluster_matrix.mean(axis=0)).flatten()
        top_term_indices = mean_tfidf.argsort()[-50:][::-1]
        top_terms = [vectorizer.get_feature_names_out()[i] for i in top_term_indices]
        cluster_top_terms[cluster_id] = top_terms

    # Save results to a file
    results = {
        "clusters": clusters,
        "top_terms": cluster_top_terms,
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Clustering results saved to {output_file}")

# Main function to run clustering and analyze clusters
def main():
    positional_index = load_positional_index()

    # Prepare the document-term matrix
    doc_ids, doc_texts = create_document_term_matrix(positional_index)

    # Cluster for number of departments
    print("Clustering for departments...")
    cluster_documents(doc_ids, doc_texts, NUM_DEPARTMENTS, "department_clusters.json")

    # Cluster for number of faculties/schools
    print("Clustering for faculties/schools...")
    cluster_documents(doc_ids, doc_texts, NUM_FACULTIES, "faculty_clusters.json")

if __name__ == "__main__":
    main()
