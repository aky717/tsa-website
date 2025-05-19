import pandas as pd                      # For reading and handling CSV data
import networkx as nx                    # For building and managing graph structures
import plotly.graph_objects as go        # For creating interactive visualizations
import os                                # For file path and folder operations
from sklearn.feature_extraction.text import TfidfVectorizer  # For converting text to numerical vectors
from sklearn.metrics.pairwise import cosine_similarity       # For calculating similarity between text vectors

# List of 100 agriculture/dev-related keywords to normalize against
CLEAN_KEYWORDS = [
    "food security", "crop yield", "soil health", "irrigation", "climate change", "drought resilience",
    "smallholder farming", "women in agriculture", "sustainable farming", "pesticide use", "nutrition access",
    "farm financing", "livestock management", "seed quality", "organic agriculture", "soil erosion",
    "farming practices", "agribusiness growth", "water access", "plant breeding", "GMO crops",
    "gender equity", "agricultural policy", "technology use", "income diversification",
    "agricultural training", "education access", "market access", "land tenure", "rural development",
    "crop rotation", "precision agriculture", "food systems", "international trade", "carbon emissions",
    "greenhouse gases", "rainfall variability", "resilient communities", "agroecology", "carbon sequestration",
    "subsidy reform", "price volatility", "poverty reduction", "malnutrition reduction", "crop loss prevention",
    "remote sensing", "data-driven farming", "climate adaptation", "weather forecasting", "supply chain resilience",
    "farm labor", "access to credit", "fertilizer use", "post-harvest losses", "food distribution systems",
    "income inequality", "water management", "plant health", "youth in farming", "land use efficiency",
    "crop diversification", "migration patterns", "urban-rural linkages", "climate resilience", "ecosystem services",
    "public health", "biodiversity loss", "soil monitoring", "animal health", "technology training",
    "digital agriculture", "policy advocacy", "financial literacy", "value chain development", "agriculture education",
    "insurance schemes", "food access equity", "biofuel production", "economic upliftment", "skills training",
    "capacity building", "crop science", "pest management", "urban agriculture", "market intelligence",
    "investment in ag", "women’s empowerment", "climate mitigation", "crop diseases", "pollution control",
    "clean technologies", "mobile extension", "farm logistics", "aquaculture systems", "seasonal forecasting",
    "youth migration", "trade agreements", "nutrition programs", "healthcare access", "rural banking"
]

# Assign specific colors for different keyword themes
CATEGORY_COLORS = {
    "climate": "#FDB863", "soil": "#B2ABD2", "tech": "#E66101", "equity": "#5E3C99",
    "water": "#4393C3", "nutrition": "#D6604D", "production": "#4DAC26", "finance": "#762A83",
    "topic": "#FFD700", "default": "#BFBFBF"
}

# Mapping of keywords to their corresponding theme categories
CATEGORY_MAP = {
    "climate": ["climate change", "climate adaptation", "carbon emissions", "carbon sequestration", "greenhouse gases",
                "rainfall variability", "climate resilience", "climate mitigation", "seasonal forecasting"],
    "soil": ["soil health", "soil erosion", "soil monitoring", "land use efficiency", "land tenure"],
    "tech": ["precision agriculture", "remote sensing", "digital agriculture", "data-driven farming", "mobile extension",
             "technology use", "technology training", "clean technologies"],
    "equity": ["gender equity", "women in agriculture", "education access", "youth in farming", "women’s empowerment"],
    "water": ["irrigation", "water access", "water management"],
    "nutrition": ["nutrition access", "malnutrition reduction", "food access equity", "nutrition programs", "public health"],
    "production": ["crop yield", "crop loss prevention", "seed quality", "fertilizer use", "pesticide use", "crop rotation", "plant breeding", "crop diversification"],
    "finance": ["farm financing", "access to credit", "insurance schemes", "subsidy reform", "rural banking"]
}

# Finds the closest keyword match from the CLEAN_KEYWORDS list using cosine similarity
def get_best_match(raw_keyword):
    vectorizer = TfidfVectorizer().fit(CLEAN_KEYWORDS + [raw_keyword])  # Fit on all known + input keyword
    vecs = vectorizer.transform([raw_keyword] + CLEAN_KEYWORDS)         # Vectorize input and all clean keywords
    sims = cosine_similarity(vecs[0:1], vecs[1:]).flatten()             # Compute similarity between input and others
    best_index = sims.argmax()                                          # Index of best match
    return CLEAN_KEYWORDS[best_index]

# Returns the color category for a given keyword
def get_category(keyword):
    for cat, kws in CATEGORY_MAP.items():
        if keyword in kws:
            return cat
    return "default"  # If no match, use default color

# Main function to generate and save the keyword network graph
def generate_keyword_network(file_path, output_folder):
    df = pd.read_csv(file_path)  # Read CSV file
    df = df.dropna(subset=['Summary topic', 'Keywords'])  # Drop rows missing required columns
    df['Keywords'] = df['Keywords'].astype(str).str.split(';')  # Split keywords by semicolon
    df_exploded = df.explode('Keywords')  # One keyword per row
    df_exploded['Keywords'] = df_exploded['Keywords'].str.strip().str.lower()  # Clean formatting

    # Get the top 5 most common summary topics
    top_topics = df_exploded['Summary topic'].value_counts().head(5).index.tolist()
    df_filtered = df_exploded[df_exploded['Summary topic'].isin(top_topics)]  # Filter for top topics

    # Match keywords to CLEAN_KEYWORDS
    df_filtered['Cleaned Keyword'] = df_filtered['Keywords'].apply(get_best_match)

    G = nx.Graph()  # Initialize an empty graph
    for _, row in df_filtered.iterrows():
        topic = row['Summary topic']
        keyword = row['Cleaned Keyword']

        G.add_node(topic, type='topic', color=CATEGORY_COLORS['topic'])  # Add topic node
        cat = get_category(keyword)  # Get category for keyword
        G.add_node(keyword, type='keyword', color=CATEGORY_COLORS.get(cat, CATEGORY_COLORS['default']))  # Add keyword node
        G.add_edge(topic, keyword)  # Create edge between topic and keyword

    # Compute node positions using force-directed layout
    pos = nx.spring_layout(G, seed=42)

    # Create edge traces for plotly
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Define how edges will appear
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines'
    )

    # Define node positions, labels, colors, and sizes
    node_x, node_y, labels, colors, sizes = [], [], [], [], []
    for node, data in G.nodes(data=True):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        labels.append(node)
        colors.append(data['color'])                          # Color based on type/category
        sizes.append(28 if data['type'] == 'topic' else 16)   # Bigger size for topic nodes

    # Create node traces for plotly
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=labels,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=colors,
            size=sizes,
            line_width=2
        )
    )

    # Combine edge and node traces into a figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text='🌐 Keyword Network by Topic (Categorized)',  # Chart title
                font=dict(size=22)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # Hide x-axis
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)   # Hide y-axis
        )
    )

    # Save figure to Visualizations folder
    vis_folder = os.path.join(output_folder, 'Visualizations')
    os.makedirs(vis_folder, exist_ok=True)  # Create folder if it doesn’t exist
    output_file = os.path.join(vis_folder, f"keyword_network_{os.path.basename(file_path).replace('.csv', '')}.html")
    fig.write_html(output_file)  # Save interactive chart as HTML
    print(f"🔗 Keyword network saved to '{output_file}'")
    return output_file  # Return path to saved file
