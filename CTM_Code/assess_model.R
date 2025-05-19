# Load required libraries
library(readr)        # For reading CSV files
library(topicmodels)  # For working with topic models like CTM
library(dplyr)        # For manipulating data frames
library(tidyr)        # For reshaping data
library(stringr)      # For string operations

# Read command-line arguments passed to the script (like filenames)
args <- commandArgs(trailingOnly = TRUE)

# Check if at least 2 arguments (RData file and input CSV) were provided
if (length(args) < 2) {
  stop("At least 2 arguments must be provided: RData file and input CSV file.")
}

# Store normalized absolute paths for the CTM model and the CSV data file
rdata_file <- normalizePath(args[1])
csv_file <- normalizePath(args[2])

# Optionally change working directory to the folder containing the CSV file
# This ensures all output files are saved in the same location as the input
setwd(dirname(csv_file))

# Load the RData file which contains the trained CTM model
load(rdata_file)  # Loads an object called `ctm`

# Read the input metadata CSV file
data <- read_csv(csv_file, show_col_types = FALSE)  # Avoid printing column types

# Extract results from the CTM model
pos <- posterior(ctm)     # Contains both topic-word and document-topic probabilities
terms <- pos$terms        # Matrix of word probabilities per topic
topics <- pos$topics      # Matrix of topic probabilities per document

# For each topic, get indices of the top 15 most probable terms
term_indices <- apply(terms, 1, function(x) order(x, decreasing = TRUE)[1:15])

# Use those indices to retrieve the actual top 15 keywords (term names)
term_labels <- apply(term_indices, 2, function(x) colnames(terms)[x])

# For each topic, get indices of the top 10 most representative documents
topic_indices <- apply(topics, 2, function(x) order(x, decreasing = TRUE)[1:10])

# Use those indices to extract the corresponding abstracts
topic_abstracts <- apply(topic_indices, 2, function(x) data$Abstract[x])

# Create a summary dataframe to hold topic info, keywords, and example abstracts
summary_df <- data.frame()

# Loop over each topic (from 1 to total number of topics in the CTM model)
for (i in 1:ctm@k) {
  topic_terms <- paste0(term_labels[, i], collapse = "; ")  # Join top 15 keywords with semicolons
  topic_row <- data.frame(Topic_Number = i, Keywords = topic_terms)  # Start row with topic number and keywords
  
  # Add the top 10 abstracts for that topic as separate columns
  for (j in 1:10) {
    topic_row[, paste0("Abstract_", j)] <- topic_abstracts[j, i]
  }
  
  # Add this row to the final summary table
  summary_df <- bind_rows(summary_df, topic_row)
}

# Add a new column showing how much of the corpus each topic covers (percentage)
summary_df$Perc_of_Corpus <- colSums(pos$topics) / sum(pos$topics) * 100

# Write outputs to CSV files in the same folder as the input CSV
write.csv(summary_df, "CTM10 - Topics With Keywords and Abstracts.csv", row.names = FALSE)  # Main summary
write.csv(pos$terms, "CTM10 - Topic Word Matrix.csv", row.names = FALSE)                   # Full term matrix
write.csv(pos$topics, "CTM10 - Doc Topic Matrix.csv", row.names = FALSE)                   # Full document-topic matrix
