#!/usr/bin/env python

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def parse_input_data(data_str):
    lines = data_str.strip().split('\n')
    data = [line.split('\t')[-1] for line in lines]  
    return data

def main():
    parser = argparse.ArgumentParser(description="Generate a stacked bar graph for species data.")
    parser.add_argument("data_file", type=str, help="Input species data file in tab-separated format.")
    args = parser.parse_args()

    # Read input data from file
    with open(args.data_file, 'r') as file:
        data_str = file.read()

    # Parse input data
    data = parse_input_data(data_str)

    # Create DataFrame from the data
    df = pd.DataFrame(data, columns=["Species"])

    # Group by species and count occurrences
    species_counts = df["Species"].value_counts()

    # Plot stacked bar graph with different colors for each species
    num_species = len(species_counts)
    colors = plt.cm.tab20.colors[:num_species]
    species_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=colors)

    # Remove x-axis ticks and labels
    plt.xticks([])

    # Create legend with species names and colors
    legend_patches = [mpatches.Patch(color=colors[i], label=species_counts.index[i]) for i in range(num_species)]
    plt.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title('Species classification')
    plt.tight_layout() 
    plt.show()

if __name__ == "__main__":
    main()





