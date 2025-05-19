# Load necessary libraries
library(dplyr)        # For data manipulation
library(readr)        # For reading CSVs
library(tm)           # For text mining (corpus, cleaning, DTM)
library(topicmodels)  # For topic modeling (CTM)
library(SnowballC)    # For stemming (reducing words to root form)

# Read command line arguments (input CSV and output file prefix)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Two arguments must be provided: input CSV and output Rdata prefix")
}

# Extract the input file path and the prefix for output RData file(s)
input_file <- args[1]
output_rdata_prefix <- args[2]

# Print input arguments for debugging
cat("Arguments provided:\n")
print(args)

# Set working directory to where the input file is located
# Ensures output files are saved in the same place
setwd(dirname(normalizePath(input_file)))
cat("Working directory set to:\n")
print(getwd())

# Load the CSV data into a dataframe
data <- read_csv(input_file, show_col_types = FALSE)  # Don't show column types

# Make sure the required 'Abstract' column is present
if (!"Abstract" %in% colnames(data)) {
  stop("Input file must have an 'Abstract' column.")
}

# Remove rows with empty or missing abstracts
data <- data %>% filter(!is.na(Abstract) & nchar(Abstract) > 0)
cat("✅ Loaded and filtered data, remaining rows:", nrow(data), "\n")

# Create a text corpus from the abstract column
corp <- VCorpus(VectorSource(data$Abstract)) %>%
  tm_map(content_transformer(tolower)) %>%              # Convert text to lowercase
  tm_map(removePunctuation, ucp = TRUE) %>%             # Remove punctuation
  tm_map(removeNumbers) %>%                             # Remove numbers
  tm_map(removeWords, c(stopwords("english"), "food", "security", "insecurity")) %>%  # Remove stopwords and common domain-specific words
  tm_map(stemDocument) %>%                              # Stem words (e.g., "growing" → "grow")
  tm_map(stripWhitespace)                               # Remove extra spaces

# Custom function to tokenize text into unigrams and bigrams
BigramTokenizer <- function(x) {
  words_list <- words(x)  # Split text into words
  bigrams <- unlist(lapply(ngrams(words_list, 2), paste, collapse = "_"), use.names = FALSE)  # Make bigrams like "climate_change"
  c(words_list, bigrams)  # Combine unigrams and bigrams
}

# Create a document-term matrix using the custom tokenizer
dtm <- DocumentTermMatrix(corp, control = list(tokenize = BigramTokenizer))

# Remove sparse terms (those that appear in very few documents)
# The threshold depends on the number of documents, but capped at 0.1
sparse_val <- max(0.1, 1 - 10/nrow(dtm))
dtm <- removeSparseTerms(dtm, sparse = sparse_val)

cat("✅ Document-term matrix created, terms:", ncol(dtm), "docs:", nrow(dtm), "\n")

# If the DTM is empty after filtering, stop and warn the user
if (ncol(dtm) == 0 || nrow(dtm) == 0) {
  stop("DTM is empty after sparsity filtering. Try adjusting the sparsity threshold or check your data.")
}

# Create a folder to store CTM model outputs (if not already present)
output_dir <- file.path(getwd(), "CTMmods")
if (!dir.exists(output_dir)) dir.create(output_dir)

# Number of topics to use for CTM (currently just 5)
ks <- 5

# Loop over each value of k (for now just one) and train the CTM model
for (k in ks) {
  cat("📌 Running CTM with", k, "topics...\n")
  ctm <- CTM(dtm, k = k, method = 'VEM')  # VEM = Variational Expectation-Maximization
  output_path <- file.path(output_dir, paste0("ctm", k, ".Rdata"))  # Save path for this model
  save(ctm, file = output_path)  # Save model to .Rdata file
  cat("✅ Saved model to", output_path, "\n")
}
