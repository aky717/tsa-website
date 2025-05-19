import pandas as pd                      # For reading and processing Excel data
import matplotlib
matplotlib.use('Agg')                   # Disable GUI backend to prevent rendering errors in non-interactive environments
import matplotlib.pyplot as plt         # For creating plots
import os                               # For file path and directory management

def line_chart_overview(file_path, output_folder):
    df = pd.read_excel(file_path)  # Load the input Excel file as a DataFrame

    # Drop rows where either 'Year' or 'Assigned Topic' is missing
    df = df.dropna(subset=['Year', 'Assigned Topic'])

    # Convert 'Year' column to integers, safely handling invalid values
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').dropna().astype(int)

    # Remove leading/trailing whitespace in topic names
    df['Assigned Topic'] = df['Assigned Topic'].str.strip()

    # Group by Year and Assigned Topic, count number of entries per group, and reshape to wide format
    topic_trends = df.groupby(['Year', 'Assigned Topic']).size().unstack(fill_value=0)

    # Create a line chart to show trends in topic counts over the years
    plt.figure(figsize=(12, 6))         # Set size of the figure
    topic_trends.plot(marker='o')       # Plot lines with circular markers at data points
    plt.title('Topic Trends Over Time') # Title of the chart
    plt.xlabel('Year')                  # Label for x-axis
    plt.ylabel('Number of Publications')# Label for y-axis
    plt.xticks(rotation=45)             # Rotate x-axis labels for better readability
    plt.tight_layout()                  # Adjust layout to avoid label clipping

    # Create a 'Visualizations' folder in the specified output folder
    vis_folder = os.path.join(output_folder, 'Visualizations')
    os.makedirs(vis_folder, exist_ok=True)  # Create folder if it doesn't exist

    # Set the output file path for the saved chart
    output_file = os.path.join(vis_folder, 'line_chart_overview.png')
    plt.savefig(output_file)  # Save the figure as a PNG image
    print(f"📈 Line chart saved to '{output_file}'")  # Notify user
    plt.close()  # Close the figure to free up memory