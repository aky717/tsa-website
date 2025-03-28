library(readr)
library(topicmodels)
library(dplyr)
library(tidyr)
library(stringr)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("At least 2 arguments must be provided: RData file and input CSV file.")
}

rdata_file <- normalizePath(args[1])
csv_file <- normalizePath(args[2])

# Optional: setwd to the CSV directory (safe for relative outputs)
setwd(dirname(csv_file))

# Load CTM model
load(rdata_file)

# Load data
data <- read_csv(csv_file, show_col_types = FALSE)

# Get topic model outputs
pos <- posterior(ctm)
terms <- pos$terms
topics <- pos$topics

# Extract top 15 keywords per topic
term_indices <- apply(terms, 1, function(x) order(x, decreasing = TRUE)[1:15])
term_labels <- apply(term_indices, 2, function(x) colnames(terms)[x])

# Extract top 10 documents (abstracts) per topic
topic_indices <- apply(topics, 2, function(x) order(x, decreasing = TRUE)[1:10])
topic_abstracts <- apply(topic_indices, 2, function(x) data$Abstract[x])

# Create summary table
summary_df <- data.frame()
for (i in 1:ctm@k) {
  topic_terms <- paste0(term_labels[, i], collapse = "; ")
  topic_row <- data.frame(Topic_Number = i, Keywords = topic_terms)
  for (j in 1:10) {
    topic_row[, paste0("Abstract_", j)] <- topic_abstracts[j, i]
  }
  summary_df <- bind_rows(summary_df, topic_row)
}

summary_df$Perc_of_Corpus <- colSums(pos$topics) / sum(pos$topics) * 100

# Always write to the same place as input file
write.csv(summary_df, "CTM10 - Topics With Keywords and Abstracts.csv", row.names = FALSE)
write.csv(pos$terms, "CTM10 - Topic Word Matrix.csv", row.names = FALSE)
write.csv(pos$topics, "CTM10 - Doc Topic Matrix.csv", row.names = FALSE)
