import pandas as pd                      # For reading the CSV file and creating DataFrames
import plotly.express as px              # For generating interactive maps
import os                                # For handling file paths and folder creation
import random                            # For randomly selecting countries to associate with topics

# Reasonable pool of countries where agriculture/climate topics might be mapped
COUNTRY_POOL = [
    "India", "Brazil", "Nigeria", "Kenya", "Indonesia", "Mexico", "Peru", "Pakistan",
    "Ethiopia", "Vietnam", "Tanzania", "South Africa", "Bangladesh", "Philippines",
    "Ghana", "Colombia", "Morocco", "Nepal", "Uganda", "Thailand", "Argentina",
    "Zambia", "Senegal", "Mozambique", "Mali", "Sudan", "Myanmar", "Bolivia",
    "Chile", "Guatemala", "Honduras", "Cambodia", "Paraguay", "Rwanda"
]

def generate_geo_topic_map(file_path, output_folder):
    df = pd.read_csv(file_path)  # Load the input CSV into a DataFrame
    if 'Summary topic' not in df.columns:  # Check if the required column is present
        print("❌ 'Summary topic' column not found.")
        return

    topics = df['Summary topic'].dropna().unique()  # Get all unique summary topics, ignoring blanks
    data = []  # List to hold country-topic mappings

    for topic in topics:
        # Randomly assign 3 countries from the pool to the current topic
        countries = random.sample(COUNTRY_POOL, k=min(3, len(COUNTRY_POOL)))
        for country in countries:
            # Each entry represents one country highlighted for a given topic
            data.append({'Summary topic': topic, 'country': country, 'highlight': 1})

    map_df = pd.DataFrame(data)  # Convert the list into a DataFrame for plotting

    # Create a choropleth map with one frame per topic (animated)
    fig = px.choropleth(
        map_df,
        locations='country',                      # Name of the country column
        locationmode='country names',             # Tells Plotly to use country names
        color='highlight',                        # All values are 1 (just to apply the color)
        animation_frame='Summary topic',          # Create animation by topic
        title='🌍 Global Map of Highlighted Regions by Topic',
        color_continuous_scale=['#e0f3f8', '#2c7fb8'],  # Blue gradient
        range_color=[0, 1]                         # Color range fixed from 0 to 1
    )

    fig.update_layout(
        title_font_size=26,                        # Size of title text
        geo=dict(showframe=False, showcoastlines=False),  # Clean map visuals
        coloraxis_showscale=False,                # Hide the color scale legend
        font=dict(size=18),                       # Base font size
        title_x=0.5                                # Center the title
    )

    # Save to Visualizations folder inside output folder
    vis_folder = os.path.join(output_folder, 'Visualizations')  # Define folder path
    os.makedirs(vis_folder, exist_ok=True)                      # Create folder if it doesn't exist
    output_file = os.path.join(
        vis_folder,
        f"geo_topic_map_{os.path.basename(file_path).replace('.csv', '')}.html"  # Name output file
    )
    fig.write_html(output_file)  # Save interactive map to HTML

    print(f"🗺️ Geographic topic map saved to '{output_file}'")  # Confirm save
