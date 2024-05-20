#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def main():
    # Step 1: Manually provide the file path
    file_path = input("Enter the file path to the data file: ")

    # Step 2: Read the data from the file into a DataFrame
    data_df = pd.read_csv(file_path, delimiter='\t', thousands=',')

    # Step 3: Manually specify the value from the confusion matrix to plot
    value_to_plot = input("Enter the column name from the confusion matrix to plot (e.g., 'accuracy'): ")

    # Step 4: Manually specify the columns for grouping
    grouping_columns = input("Enter the column names for grouping separated by commas (e.g., 'classifier,read_number,read_length'): ").split(',')

    # Step 5: Manually specify the chart name
    chart_name = input("Enter the chart name: ")

    # Step 6: Ask for the chart type choice (box plot or violin plot)
    chart_type_choice = input("Enter 'box' for box plot or 'violin' for violin plot: ").strip().lower()

    plt.figure(figsize=(12, 6))

    # Step 8: Specify the column for custom color mapping
    color_column = input("Enter the column name for custom color mapping: ")

    # Step 9: Create a color map based on unique values in the color column
    unique_colors = data_df[color_column].unique()
    color_map = cm.tab20(np.linspace(0, 1, len(unique_colors)))

    # Group data based on the specified grouping columns
    grouped_data = data_df.groupby(grouping_columns)

    # Create labels for each group
    group_labels = [', '.join(str(val) for val in group) for group, _ in grouped_data]

    for i, (_, group_data) in enumerate(grouped_data):
        # Step 7: Assign a color to each group based on the color_column
        group_color = color_map[unique_colors.tolist().index(group_data[color_column].iloc[0])]

        if chart_type_choice == 'box':
            parts = plt.boxplot(group_data[value_to_plot], positions=[i + 1], showfliers=False, patch_artist=True)
            for box in parts['boxes']:
                box.set(facecolor=group_color, alpha=0.7)
        elif chart_type_choice == 'violin':
            parts = plt.violinplot(group_data[value_to_plot], positions=[i + 1], showmedians=True, showextrema=False)
            for pc in parts['bodies']:
                pc.set_facecolor(group_color)
                pc.set_edgecolor('black')
                pc.set_alpha(0.7)
        else:
            raise ValueError("Invalid chart type choice. Please enter 'box' or 'violin'.")

    # Set the x-axis labels based on the grouping labels
    plt.xticks(range(1, len(group_labels) + 1), group_labels, rotation=45, ha='right')

    plt.xlabel(", ".join(col.capitalize() for col in grouping_columns))
    plt.ylabel(value_to_plot.capitalize())
    plt.title(chart_name)  # Use the manually specified chart name
    plt.grid(True)
    plt.tight_layout()

    # Step 7: Move the legend to the right side of the graph
    custom_patches = [plt.Rectangle((0, 0), 1, 1, fc=color_map[i], label=unique_colors[i]) for i in range(len(unique_colors))]
    plt.legend(handles=custom_patches, loc='center left', bbox_to_anchor=(1, 0.5), title=color_column.capitalize())

    plt.show()

if __name__ == '__main__':
    main()



