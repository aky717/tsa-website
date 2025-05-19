import pandas as pd                # For loading and manipulating Excel data
import os                          # For file path and folder operations
import matplotlib
matplotlib.use('Agg')             # Disable GUI backend to avoid RuntimeErrors (important on headless servers)
import matplotlib.pyplot as plt   # For plotting bar charts

def bar_chart_overview(file_path, output_folder):
    # Load Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Remove rows where either 'Year' or 'Assigned Topic' is missing
    df = df.dropna(subset=['Year', 'Assigned Topic'])

    # Convert 'Year' to integer type, forcing non-numeric to NaN and then dropping them
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').dropna().astype(int)

    # Strip extra whitespace from topic names
    df['Assigned Topic'] = df['Assigned Topic'].str.strip()

    # Count how many times each topic appears
    topic_counts = df['Assigned Topic'].value_counts()

    # Create a bar chart
    plt.figure(figsize=(10, 6))               # Set the size of the chart
    topic_counts.plot(kind='bar')            # Plot a vertical bar chart
    plt.title('Count of Publications by Assigned Topic')  # Chart title
    plt.xlabel('Assigned Topic')             # X-axis label
    plt.ylabel('Number of Publications')     # Y-axis label
    plt.xticks(rotation=45)                  # Rotate x labels for better readability
    plt.tight_layout()                       # Adjust layout to prevent clipping

    # Create a Visualizations folder inside the output folder (if not already there)
    vis_folder = os.path.join(output_folder, 'Visualizations')
    os.makedirs(vis_folder, exist_ok=True)

    # Save the plot to the folder
    output_file = os.path.join(vis_folder, 'bar_chart_overview.png')
    plt.savefig(output_file)  # Save chart as PNG
    print(f"📊 Bar chart saved to '{output_file}'")
    plt.close()  # Close the figure to free memory
