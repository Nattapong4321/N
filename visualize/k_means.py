#!/usr/bin/env python

import sys
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from Bio import SeqIO

# Function to convert FASTQ sequences to k-mer counts
def seq_to_kmer_counts(sequences, k):
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(k, k))
    X = vectorizer.fit_transform(sequences)
    return X.toarray()

# Function to create output directory if it doesn't exist
def create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

if __name__ == "__main__":
    # Check if correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <fastq_file> <num_clusters> <output_dir>")
        sys.exit(1)

    # Read command-line arguments
    fastq_file = sys.argv[1]
    num_clusters = int(sys.argv[2])
    output_dir = sys.argv[3]

    # Create output directory if it doesn't exist
    create_output_dir(output_dir)

    # Load FASTQ sequences
    sequences = []
    for record in SeqIO.parse(fastq_file, "fastq"):
        sequences.append(str(record.seq))

    # Convert sequences to k-mer counts
    k = 6  # Choose an appropriate k-mer length
    X = seq_to_kmer_counts(sequences, k)

    # Perform k-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X)

    # Get cluster assignments
    cluster_labels = kmeans.labels_

    # Reduce dimensionality for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # Plot clustering results
    plt.figure(figsize=(8, 6))
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    for i in range(num_clusters):
        plt.scatter(X_pca[cluster_labels == i, 0], X_pca[cluster_labels == i, 1], c=colors[i % len(colors)], label=f'Cluster {i+1}')
    plt.title('Clustering Results')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'clustering_result.png'))
    plt.close()

    # Output the representative sequences from each cluster
    clusters = {}
    for i, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(sequences[i])

    # Write representative sequences to a FASTA file
    fasta_file = os.path.join(output_dir, 'representative_sequences.fasta')
    with open(fasta_file, 'w') as f:
        for label, cluster_seqs in clusters.items():
            representative_seq = cluster_seqs[np.random.randint(0, len(cluster_seqs))]
            f.write(f'>Cluster_{label+1}\n{representative_seq}\n')

    print("Clustering result saved as clustering_result.png in", output_dir)
    print("Representative sequences saved as representative_sequences.fasta in", output_dir)