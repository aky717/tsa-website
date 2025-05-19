library(readr)
library(topicmodels)
library(dplyr)
library(tidyr)
library(stringr)

# ---- Parse Arguments ----
args <- commandArgs(trailingOnly = TRUE)

# Check if at least 2 arguments (RData file and input CSV) were provided
if (length(args) < 2) {
  stop("At least 2 arguments must be provided: RData file and input CSV file.")
}

# Store normalized absolute paths for the CTM model and the CSV data file
rdata_file <- normalizePath(args[1])
csv_file <- normalizePath(args[2])

# ---- Set Output Directory Based on RData File ----
output_dir <- dirname(rdata_file)

# ---- Load Model and Data ----
load(rdata_file)  # loads `ctm`
data <- read_csv(csv_file, show_col_types = FALSE)

# ---- Posterior Calculation ----
pos <- posterior(ctm)
terms <- pos$terms
topics <- pos$topics

# ---- Top Terms per Topic ----
term_indices <- apply(terms, 1, function(x) order(x, decreasing = TRUE)[1:15])

# Use those indices to retrieve the actual top 15 keywords (term names)
term_labels <- apply(term_indices, 2, function(x) colnames(terms)[x])

# ---- Top Abstracts per Topic ----
topic_indices <- apply(topics, 2, function(x) order(x, decreasing = TRUE)[1:10])

# Use those indices to extract the corresponding abstracts
topic_abstracts <- apply(topic_indices, 2, function(x) data$Abstract[x])

# ---- Construct Summary ----
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

# ---- Write Outputs to Output Dir ----
write.csv(summary_df, file = file.path(output_dir, "CTM10 - Topics With Keywords and Abstracts.csv"), row.names = FALSE)
write.csv(pos$terms, file = file.path(output_dir, "CTM10 - Topic Word Matrix.csv"), row.names = FALSE)
write.csv(pos$topics, file = file.path(output_dir, "CTM10 - Doc Topic Matrix.csv"), row.names = FALSE)

cat("✅ All CTM summary outputs written to:", output_dir, "\n")

# library(readr)
# library(topicmodels)
# library(dplyr)
# library(tidyr)
# library(stringr)

# args <- commandArgs(trailingOnly = TRUE)

# if (length(args) < 2) {
#   stop("At least 2 arguments must be provided: RData file and input CSV file.")
# }

# rdata_file <- normalizePath(args[1])
# csv_file <- normalizePath(args[2])

# # Optional: setwd to the CSV directory (safe for relative outputs)
# setwd(dirname(csv_file))

# # Load CTM model
# load(rdata_file)

# # Load data
# data <- read_csv(csv_file, show_col_types = FALSE)

# # Get topic model outputs
# pos <- posterior(ctm)
# terms <- pos$terms
# topics <- pos$topics

# # Extract top 15 keywords per topic
# term_indices <- apply(terms, 1, function(x) order(x, decreasing = TRUE)[1:15])
# term_labels <- apply(term_indices, 2, function(x) colnames(terms)[x])

# # Extract top 10 documents (abstracts) per topic
# topic_indices <- apply(topics, 2, function(x) order(x, decreasing = TRUE)[1:10])
# topic_abstracts <- apply(topic_indices, 2, function(x) data$Abstract[x])

# # Create summary table
# summary_df <- data.frame()
# for (i in 1:ctm@k) {
#   topic_terms <- paste0(term_labels[, i], collapse = "; ")
#   topic_row <- data.frame(Topic_Number = i, Keywords = topic_terms)
#   for (j in 1:10) {
#     topic_row[, paste0("Abstract_", j)] <- topic_abstracts[j, i]
#   }
#   summary_df <- bind_rows(summary_df, topic_row)
# }

# summary_df$Perc_of_Corpus <- colSums(pos$topics) / sum(pos$topics) * 100

# # Always write to the same place as input file
# write.csv(summary_df, "CTM10 - Topics With Keywords and Abstracts.csv", row.names = FALSE)
# write.csv(pos$terms, "CTM10 - Topic Word Matrix.csv", row.names = FALSE)
# write.csv(pos$topics, "CTM10 - Doc Topic Matrix.csv", row.names = FALSE)
