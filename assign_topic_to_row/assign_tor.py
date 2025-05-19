# Modified Assign to Topic Code (no keywords required)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    """Remove extra spaces and normalize text formatting."""
    if pd.isna(text):
        return ''
    return ' '.join([word.strip() for word in str(text).split() if word.strip()])

def assign_topics_to_metadata(metadata_file, topics_file, output_file):
    # Load the metadata file (support both CSV and Excel)
    df = pd.read_csv(metadata_file) if metadata_file.endswith(".csv") else pd.read_excel(metadata_file)
    topics_df = pd.read_csv(topics_file) if topics_file.endswith(".csv") else pd.read_excel(topics_file)

    # Limit to top 5 topics for testing
    topics_df = topics_df.head(5)

    # Check required columns
    if 'Title' not in df.columns:
        raise ValueError("The metadata file must contain the 'Title' column.")
    if 'Summary topic' not in topics_df.columns or 'Keywords' not in topics_df.columns:
        raise ValueError("The topics file must contain 'Summary topic' and 'Keywords' columns.")

    # Clean title and topic keywords
    df['Title'] = df['Title'].apply(clean_text)
    topics_df['Keywords'] = topics_df['Keywords'].apply(clean_text)

    # TF-IDF vectorization
    combined = df['Title'].tolist() + topics_df['Keywords'].tolist()
    vectorizer = TfidfVectorizer().fit_transform(combined)
    metadata_vectors = vectorizer[:len(df)]
    topic_vectors = vectorizer[len(df):]

    # Cosine similarity
    similarities = cosine_similarity(metadata_vectors, topic_vectors)
    topic_labels = topics_df['Summary topic'].tolist()

    # Assign closest topic
    df['Assigned Topic'] = [topic_labels[similarities[i].argmax()] for i in range(len(df))]

    # Save output
    df.to_excel(output_file, index=False, engine='xlsxwriter')
    print(f"✅ Assigned topics saved to: {output_file}")
    return output_file
