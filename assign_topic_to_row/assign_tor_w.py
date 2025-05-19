import pandas as pd  # For handling Excel files and dataframes
from sklearn.feature_extraction.text import TfidfVectorizer  # To convert text to numerical vectors
from sklearn.metrics.pairwise import cosine_similarity  # To measure similarity between vectors

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
    """
    Assigns a topic to each row in the metadata based on similarity
    between its title and the keywords of each topic using TF-IDF and cosine similarity.
    """

    # Prompt user for file names (without .xlsx extension)
    metadata_file = input("Enter the name of the metadata file (without extension): ")
    topics_file = input("Enter the name of the topics file (without extension): ")

    # Read the metadata and topic keyword files
    df = pd.read_excel(f"/home/anika/work/mine-food-security/visualize/{metadata_file}.xlsx")
    topics_df = pd.read_excel(f"/home/anika/work/mine-food-security/visualize/{topics_file}.xlsx")

    # Check if necessary columns exist
    if 'Title' not in df.columns:
        raise ValueError("The metadata file must contain the 'Title' column.")
    if 'Summary topic' not in topics_df.columns or 'Keywords' not in topics_df.columns:
        raise ValueError("The topics file must contain 'Summary topic' and 'Keywords' columns.")

    # Clean all titles to make comparison more accurate
    df['Title'] = df['Title'].apply(clean_text)

    # Clean all keyword sets in the topics file
    topics_df['Keywords'] = topics_df['Keywords'].apply(clean_text)

    # Create a list of all topic labels like ["food security", "water management", ...]
    topic_labels = topics_df['Summary topic'].tolist()

    # Create a list of keyword strings like ["food, nutrition, hunger", "irrigation, drought", ...]
    topic_keywords = topics_df['Keywords'].tolist()

    # Combine all cleaned titles + topic keyword strings into one list
    # This is needed so TF-IDF can process them all together
    combined_titles = df['Title'].tolist() + topic_keywords

    # Turn the combined list into TF-IDF vectors (numerical representation of the words)
    vectorizer = TfidfVectorizer().fit_transform(combined_titles)

    # Slice the vector matrix:
    # The first N rows are metadata titles
    metadata_vectors = vectorizer[:len(df)]
    # The remaining rows are topic keyword strings
    topic_vectors = vectorizer[len(df):]

    # Compare every title vector with every topic keyword vector
    # Each row in 'similarities' is a list of how similar that title is to every topic
    similarities = cosine_similarity(metadata_vectors, topic_vectors)

    # For each title row, find the index of the most similar topic keyword vector
    # Then grab the corresponding topic label using that index
    topic_assignments = [
        topic_labels[similarities[i].argmax()] for i in range(len(df))
    ]

    # Add the topic label to a new column in the metadata
    df['Assigned Topic'] = topic_assignments

    # Save the updated metadata to a new Excel file
    output_file = f"/home/anika/work/mine-food-security/visualize/{metadata_file}_with_assigned_topics.xlsx"
    df.to_excel(output_file, index=False, engine='xlsxwriter')  # Save without row numbers

    # Let the user know where the file is saved
    print(f"Assigned topics saved to '{output_file}'.")

# Run the function
assign_topics_to_metadata()
