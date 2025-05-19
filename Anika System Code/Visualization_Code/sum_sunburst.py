import pandas as pd                      # For data loading and manipulation
import plotly.express as px              # For creating interactive sunburst charts
import os                                # For file and directory operations
from difflib import get_close_matches    # For fuzzy string matching to map keywords

# List of 100 curated agricultural/development keywords
GOOD_KEYWORDS = [
    "agriculture", "climate change", "soil", "crop", "farmer", "irrigation", "yield", "resilience", "pesticide",
    "food security", "gender", "sustainability", "fertilizer", "drought", "farming systems", "smallholder",
    "rainfall", "carbon", "ecosystem", "nutrition", "biodiversity", "income", "market access", "land use",
    "subsidy", "rural development", "organic farming", "mechanization", "plant disease", "livestock", "carbon footprint",
    "supply chain", "seed", "agroforestry", "technology", "precision agriculture", "genetics", "GMOs", "pollination",
    "aquaculture", "water stress", "crop diversification", "microfinance", "access to credit", "education", "deforestation",
    "population growth", "renewable energy", "solar irrigation", "malnutrition", "migration", "urban agriculture",
    "labor", "income stabilization", "farm size", "training", "insurance", "weather forecasting", "global warming",
    "conflict", "policy", "cooperative", "digital tools", "climate finance", "land tenure", "crop insurance",
    "food systems", "pest management", "climate adaptation", "remittances", "data collection", "machine learning",
    "youth in agriculture", "women in agriculture", "health", "investment", "afforestation", "sub-Saharan Africa",
    "southeast Asia", "water harvesting", "crop modeling", "extension services", "soil salinity", "monitoring",
    "value chains", "sustainable intensification", "greenhouse gases", "input costs", "climate-smart ag",
    "plant breeding", "policy reform", "co-design", "conservation", "climate policy", "indigenous knowledge",
    "water availability", "technology adoption", "knowledge transfer", "disease outbreaks", "crop calendar"
]

# Function to match a keyword to the closest keyword from GOOD_KEYWORDS using fuzzy logic
def match_keyword(word):
    match = get_close_matches(word.lower(), GOOD_KEYWORDS, n=1, cutoff=0.6)
    return match[0] if match else None  # Return the best match, or None if no match passes the cutoff

# Function to generate a sunburst chart from the input CSV file
def create_sunburst_chart(file_path, output_folder):
    df = pd.read_csv(file_path)  # Load input CSV

    # Ensure required columns are present
    if "Summary topic" not in df.columns or "Keywords" not in df.columns:
        print("The file must contain 'Summary topic' and 'Keywords' columns.")
        return

    # Split keywords into a list and clean them
    df['Keywords'] = df['Keywords'].astype(str).str.split(';')
    df_exploded = df.explode('Keywords')  # Turn each keyword into its own row
    df_exploded['Keywords'] = df_exploded['Keywords'].str.strip().str.lower()  # Clean whitespace and lowercase

    # Map each keyword to a curated keyword (or discard if no match)
    df_exploded['Mapped Keyword'] = df_exploded['Keywords'].apply(match_keyword)
    df_exploded = df_exploded.dropna(subset=["Mapped Keyword"])  # Drop rows where no good match was found

    # Group by topic and keyword, count frequency, and sort
    top_keywords_per_topic = (
        df_exploded.groupby(['Summary topic', 'Mapped Keyword'])
        .size().reset_index(name='Count')
        .sort_values(['Summary topic', 'Count'], ascending=[True, False])
    )

    final_rows = []
    for topic in top_keywords_per_topic['Summary topic'].unique():
        keywords = top_keywords_per_topic[top_keywords_per_topic['Summary topic'] == topic]
        top5 = keywords.head(5)  # Get top 5 keywords per topic

        # If less than 5, fill with unused curated keywords
        used = set(top5['Mapped Keyword'])
        needed = 5 - len(top5)
        if needed > 0:
            fillers = [k for k in GOOD_KEYWORDS if k not in used][:needed]
            for f in fillers:
                top5 = pd.concat([top5, pd.DataFrame([{"Summary topic": topic, "Mapped Keyword": f, "Count": 1}])])
        final_rows.append(top5)

    final_df = pd.concat(final_rows)  # Combine all topic-keyword rows

    # Create the sunburst chart using Plotly
    fig = px.sunburst(
        final_df,
        path=["Summary topic", "Mapped Keyword"],  # Hierarchical structure
        values="Count",                           # Size of each slice based on count
        title="Sunburst Chart of Summary Topics and Keywords"
    )

    # Customize chart layout
    fig.update_layout(
        title_font_size=26,
        font=dict(size=18),
        title_x=0.5  # Center the title
    )

    # Ensure output folder exists
    vis_folder = os.path.join(output_folder, "Visualizations")
    os.makedirs(vis_folder, exist_ok=True)

    # Build the output file name based on the input file
    output_file = os.path.join(vis_folder, f"sunburst_chart_{os.path.basename(file_path).replace('.csv', '')}.html")

    # Save the chart as an interactive HTML file
    fig.write_html(output_file)
    print(f"🌞 Sunburst chart saved to '{output_file}'")
