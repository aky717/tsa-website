# use this Assign to Topic Code if keywords are NOT available
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    """Remove extra spaces and normalize text formatting."""
    if pd.isna(text):
        return ''
    return ' '.join([word.strip() for word in text.split() if word.strip()])

def assign_topics_to_metadata():
    # Step 1: Input the filenames
    metadata_file = input("Enter the name of the metadata file (without extension): ")
    topics_file = input("Enter the name of the topics file (without extension): ")

    # Load the metadata and topics files using read_excel
    df = pd.read_excel(f"/home/anika/work/mine-food-security/visualize/{metadata_file}.xlsx")
    topics_df = pd.read_excel(f"/home/anika/work/mine-food-security/visualize/{topics_file}.xlsx")

    # Ensure necessary columns are present
    if 'Title' not in df.columns:
        raise ValueError("The metadata file must contain the 'Title' column.")
    if 'Summary topic' not in topics_df.columns or 'Keywords' not in topics_df.columns:
        raise ValueError("The topics file must contain 'Summary topic' and 'Keywords' columns.")

    # Step 2: Clean and preprocess the 'Title' column
    df['Title'] = df['Title'].apply(clean_text)

    # Step 3: Clean and preprocess the topic keywords
    topics_df['Keywords'] = topics_df['Keywords'].apply(clean_text)

    # Create lists of topic labels and their keywords
    topic_labels = topics_df['Summary topic'].tolist()
    topic_keywords = topics_df['Keywords'].tolist()

    # Step 4: Combine metadata and topic keywords for vectorization
    combined_titles = df['Title'].tolist() + topic_keywords

    # Step 5: Use TF-IDF to vectorize the titles
    vectorizer = TfidfVectorizer().fit_transform(combined_titles)
    metadata_vectors = vectorizer[:len(df)]  # Metadata title vectors
    topic_vectors = vectorizer[len(df):]     # Topic keyword vectors

    # Step 6: Calculate cosine similarity between metadata titles and topic keywords
    similarities = cosine_similarity(metadata_vectors, topic_vectors)

    # Step 7: Assign the most similar topic to each row
    topic_assignments = [
        topic_labels[similarities[i].argmax()] for i in range(len(df))
    ]

    # Step 8: Add the assigned topics to the metadata DataFrame
    df['Assigned Topic'] = topic_assignments

    # Step 9: Save the updated DataFrame with assigned topics
    output_file = f"/home/anika/work/mine-food-security/visualize/{metadata_file}_with_assigned_topics.xlsx"
    df.to_excel(output_file, index=False, engine='xlsxwriter')

    print(f"Assigned topics saved to '{output_file}'.")

# Run the function
assign_topics_to_metadata()

