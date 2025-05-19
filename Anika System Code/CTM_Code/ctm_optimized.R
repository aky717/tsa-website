#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(tm)
library(topicmodels)
library(NLP)
library(textstem)  # ✅ Added for lemmatization

# ---- Parse Args ----
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("Three arguments must be provided: input CSV, output Rdata prefix, and output directory.")
}

input_file <- normalizePath(args[1])
output_rdata_prefix <- args[2]
output_dir <- normalizePath(args[3])

# ---- Load Data ----
data <- read_csv(input_file, show_col_types = FALSE)

# Make sure the required 'Abstract' column is present
if (!"Abstract" %in% colnames(data)) {
  stop("❌ Error: Input file must contain an 'Abstract' column.")
}

# Remove rows with empty or missing abstracts
data <- data %>% filter(!is.na(Abstract) & nchar(Abstract) > 0)
cat("✅ Loaded and filtered data — rows retained:", nrow(data), "\n")

# ---- Preprocess ----
corp <- VCorpus(VectorSource(data$Abstract)) %>%
  tm_map(content_transformer(tolower)) %>%
  tm_map(removePunctuation, ucp = TRUE) %>%
  tm_map(removeNumbers) %>%
  tm_map(removeWords, c(stopwords("english"), "food", "security", "insecurity")) %>%
  tm_map(content_transformer(lemmatize_strings)) %>%  # ✅ Replaced stemDocument with lemmatizer
  tm_map(stripWhitespace)

# ---- Tokenizer ----
BigramTokenizer <- function(x) {
  words_list <- words(x)  # Split text into words
  bigrams <- unlist(lapply(ngrams(words_list, 2), paste, collapse = "_"), use.names = FALSE)  # Make bigrams like "climate_change"
  c(words_list, bigrams)  # Combine unigrams and bigrams
}

# ---- Document-Term Matrix ----
dtm <- DocumentTermMatrix(corp, control = list(tokenize = BigramTokenizer))

# ---- Filter Sparse Terms ----
sparse_val <- max(0.1, 1 - 10/nrow(dtm))
dtm <- removeSparseTerms(dtm, sparse = sparse_val)
cat("📊 DTM created — terms:", ncol(dtm), " | docs:", nrow(dtm), "\n")

# If the DTM is empty after filtering, stop and warn the user
if (ncol(dtm) == 0 || nrow(dtm) == 0) {
  stop("❌ DTM is empty after filtering. Adjust sparsity threshold or check data.")
}

# ---- Create Output Folder ----
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

# ---- Run CTM ----
k <- 5  # number of topics
cat("🧠 Running CTM with", k, "topics...\n")
ctm <- CTM(dtm, k = k, method = "VEM")

# ---- Save Model ----
output_path <- file.path(output_dir, "CTMmods", paste0(output_rdata_prefix, ".Rdata"))
if (!dir.exists(dirname(output_path))) dir.create(dirname(output_path), recursive = TRUE)

save(ctm, file = output_path)
cat("✅ CTM model saved to", output_path, "\n")
