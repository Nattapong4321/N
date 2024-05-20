#!/usr/bin/env python

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec
import os  # Import the os module for working with directories

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate confusion matrix graph.')
parser.add_argument('input_file', type=str, help='Path to the input data file')
parser.add_argument('--parameter', type=str, default='accuracy', help='Confusion matrix parameter to plot')
parser.add_argument('--title', type=str, default='Confusion Matrix Analysis', help='Title for the graph')
parser.add_argument('--output_dir', type=str, default='output', help='Output directory for saving the figure')
args = parser.parse_args()

# Load data from the input file
data = pd.read_csv(args.input_file, delimiter='\t')

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

# Get unique read numbers and classifiers
read_numbers = data['read_number'].unique()
classifiers = data['classifier'].unique()

# Assign different colors
colors = plt.cm.rainbow_r(np.linspace(0, 1, len(read_numbers)))

# Create subplots with fixed positions using GridSpec
fig = plt.figure(figsize=(15, 9))  # Adjust the figure size
gs = GridSpec(3, 2, height_ratios=[1, 1, 1], hspace=0.5, wspace=0.5)  # 3 rows, 2 columns

# Set the title for the entire figure
fig.suptitle(args.title, fontsize=20)

# Define the order of classifiers
classifier_order = ['Blast', 'Kraken2', 'Centrifuge', 'EPI2ME', 'N']

# Define the common x-axis limit
x_limit = (0, 25000)  # Set the x-axis limit from 0 to 20000

# Define the x-axis ticks
x_ticks = np.arange(0, 20001, 5000)  # Include ticks at 0, 5000, 10000, 15000, and 20000

# Loop through each classifier and create a subplot
for idx, classifier in enumerate(classifier_order):
    row = idx // 2  # Determine the row
    col = idx % 2  # Determine the column
    ax = fig.add_subplot(gs[row, col])

    # Plot each read number with corresponding color
    for i, read_number in enumerate(read_numbers):
        subset = data[(data['classifier'] == classifier) & (data['read_number'] == read_number)]
        scatter = ax.scatter(subset['read_length'], np.minimum(subset[args.parameter], 100),  # Limit to 100
                            s=70,
                            marker=classifier_markers[classifier],
                            color=colors[i], label=f'{read_number}')

    ax.set_xlabel('Read Length')
    ax.set_ylabel(args.parameter.capitalize())
    ax.set_title(classifier, fontsize=18)

    # Set the common x-axis limit
    ax.set_xlim(x_limit)

    # Set the x-axis ticks
    ax.set_xticks(x_ticks)

    # Set the axis tick format to show two decimal places
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))  # Two decimal places for y-axis

    # Move legend outside the box, adjusting the position and font size
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1),
                    fontsize='x-small', title='Read Numbers')
    legend.set_bbox_to_anchor((1.02, 1))
    legend.get_title().set_fontsize('x-small')

    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# Save the figure to the specified output directory
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(args.output_dir)





