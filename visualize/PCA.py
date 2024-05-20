#!/usr/bin/env python

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Prompt the user to enter the input file path
input_file = input("Enter the input file path (CSV format): ")

try:
    # Load the data from the specified input file into a DataFrame with a tab delimiter
    data = pd.read_csv(input_file, delimiter='\t')
except FileNotFoundError:
    print("File not found. Please make sure the file exists and the path is correct.")
    exit(1)

# Print the column names to help you identify the correct ones
print("Available columns in the dataset:")
print(data.columns)

# Prompt the user to specify the x, y, z, grouping, and clustering columns
x_column = input("Enter the x-axis column name: ")
y_column = input("Enter the y-axis column name: ")
z_column = input("Enter the z-axis column name: ")
group_column = input("Enter the grouping column name: ")
cluster_column = input("Enter the clustering column name: ")

# Check if the specified columns exist in the dataset
if (
    x_column not in data.columns
    or y_column not in data.columns
    or z_column not in data.columns
    or group_column not in data.columns
    or cluster_column not in data.columns
):
    print("One or more specified columns do not exist in the dataset.")
    exit(1)

# Create a DataFrame with the x, y, z, grouping, and clustering columns
xyz_data = data[[x_column, y_column, z_column]]
group_data = data[group_column]
cluster_data = data[cluster_column]

# Standardize the data (mean=0, std=1)
xyz_data = (xyz_data - xyz_data.mean()) / xyz_data.std()

# Perform clustering (e.g., using K-Means)
num_clusters = len(cluster_data.unique())
kmeans = KMeans(n_clusters=num_clusters)
cluster_data['cluster'] = kmeans.fit_predict(xyz_data)

# Fit a PCA model to the clustered data
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(xyz_data)

# Create a new DataFrame with the first two principal components and the cluster and group columns
pca_df = pd.DataFrame(data=principalComponents, columns=['PC1', 'PC2'])
pca_df['Cluster'] = cluster_data
pca_df['Group'] = group_data

# Plot the 2D PCA graph with colors indicating clusters
plt.figure(figsize=(10, 8))
sns.scatterplot(x='PC1', y='PC2', hue='Cluster', data=pca_df, palette='viridis')
plt.title('2D PCA Dimension Reduction with Clustering')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()


