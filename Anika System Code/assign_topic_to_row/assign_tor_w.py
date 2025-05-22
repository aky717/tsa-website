import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    """
    Cleans text by:
    - Removing NaNs (turns them into empty string)
    - Removing extra spaces between words
    """
    if pd.isna(text):  # If the cell is empty or NaN
        return ''
    # Splits text into words, strips spaces from each, removes empty strings, rejoins
    return ' '.join([word.strip() for word in text.split() if word.strip()])

def assign_topics_to_metadata():
    # Get the current working directory
    cwd = os.getcwd()

    # Ask user for filenames (assume .xlsx extension)
    metadata_file = input("Enter the name of the metadata file (without extension): ").strip()
    topics_file = input("Enter the name of the topics file (without extension): ").strip()

    # Build full file paths
    metadata_path = os.path.join(cwd, f"{metadata_file}.xlsx")
    topics_path = os.path.join(cwd, f"{topics_file}.xlsx")

    # Load the files
    df = pd.read_excel(metadata_path)
    topics_df = pd.read_excel(topics_path)

    # Check if necessary columns exist
    if 'Title' not in df.columns:
        raise ValueError("The metadata file must contain the 'Title' column.")
    if 'Summary topic' not in topics_df.columns or 'Keywords' not in topics_df.columns:
        raise ValueError("The topics file must contain 'Summary topic' and 'Keywords' columns.")

    # Clean and preprocess text
    df['Title'] = df['Title'].apply(clean_text)
    topics_df['Keywords'] = topics_df['Keywords'].apply(clean_text)

    # Vectorize titles and keywords
    topic_labels = topics_df['Summary topic'].tolist()

    # Create a list of keyword strings like ["food, nutrition, hunger", "irrigation, drought", ...]
    topic_keywords = topics_df['Keywords'].tolist()
    combined_titles = df['Title'].tolist() + topic_keywords

    vectorizer = TfidfVectorizer().fit_transform(combined_titles)
    metadata_vectors = vectorizer[:len(df)]
    topic_vectors = vectorizer[len(df):]

    # Compute similarities and assign topics
    similarities = cosine_similarity(metadata_vectors, topic_vectors)
    df['Assigned Topic'] = [
        topic_labels[similarities[i].argmax()] for i in range(len(df))
    ]

    # Save result
    output_path = os.path.join(cwd, f"{metadata_file}_with_assigned_topics.xlsx")
    df.to_excel(output_path, index=False, engine='xlsxwriter')
    print(f"✅ Assigned topics saved to: {output_path}")

# Run the function
assign_topics_to_metadata()