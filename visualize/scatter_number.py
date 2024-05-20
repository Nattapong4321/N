#!/usr/bin/env python

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate confusion matrix graph.')
parser.add_argument('input_file', type=str, help='Path to the input data file')
parser.add_argument('--parameter', type=str, default='accuracy', help='Confusion matrix parameter to plot')
parser.add_argument('--title', type=str, default='Confusion Matrix Analysis', help='Title for the graph')
args = parser.parse_args()

# Load data from the input file
data = pd.read_csv(args.input_file, delimiter='\t')

# Get unique read lengths
read_lengths = data['read_length'].unique()

# Set up seaborn style
sns.set(style="whitegrid")

# Map classifier names to specific markers
classifier_markers = {
    'N': '*',
    'Kraken2': '.',
    'Blast': '+',
    'Centrifuge': 'x',
    'EPI2ME': '^'
}

# Create a scatter plot
plt.figure(figsize=(12, 6))

# Assign different colors to read lengths
colors = plt.cm.rainbow_r(np.linspace(0, 1, len(read_lengths)))

# Iterate over classifiers
for classifier in data['classifier'].unique():
    for i, read_length in enumerate(read_lengths):
        subset = data[(data['classifier'] == classifier) & (data['read_length'] == read_length)]
        scatter = plt.scatter(subset['read_number'], subset[args.parameter],
                              s=100, marker=classifier_markers[classifier],
                              color=colors[i], label=f'{classifier} (Read Length: {read_length})')

plt.xlabel('Read Number')
plt.ylabel(args.parameter.capitalize())
plt.title(args.title)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.grid(True)
plt.tight_layout()

plt.show()
