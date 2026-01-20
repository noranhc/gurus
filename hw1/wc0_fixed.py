#!/usr/bin/env python3 -B
"""Word frequency counter - the messy version"""

"""
AQ1: Separation of Concerns (SoC)
Separated the code into Model and Presentation layers.

AQ2: Single Responsibility Principle (SRP)
Divided the big function into smaller functions
< 10 lines of code each and responsible for a single task.

AQ3: Mechanism vs Policy
Previously, punctuation and stopword rules were hardcoded
inside the counting mechanism. 
The test rules were extraded into CONFIG and passed into 
pure functions. 
"""

CONFIG = {
  "input_file": "essay.txt",
  "stopwards_file": "stopwords.txt",
  "punctuation": '.,!?;:"()[]',
  "top_n": 10,
  "bar_char": "*",
  "word_width": 15
}

#--- MODEL LAYER (Pure business logic, no I/O) ---

# Load file content
def load_file(file):
  with open(file) as f:
    return f.read()
  
# Load stopwords
def load_stopwords(file):
  with open(file) as f:
    return set(line.strip() for line in f)

# Normalize casing 
def normalize(text):
  return text.lower()

# Split text into words
def tokenize(text):
  return text.split()

# Strips words from punctuations
def clean_word(word, punctuation):
  return word.strip(punctuation)

# Process text to get word counts
# Returns a list of words and their frequencies
def get_counts(words, stopwords, punctuation):
  counts = {}

  for w in words:
    w = clean_word(w, punctuation)
    if w and w not in stopwords:
      counts[w] = counts.get(w, 0) + 1
    
  return counts

# Sorts list based on counts
def sort_counts(counts):
  return sorted(counts.items(), key=lambda x: x[1], reverse=True)

# Returns the total number of words in text
def total_words(counts):
  return sum(counts.values())

#--- PRESENTATION LAYER (I/O only, no logic) ---

# Print header
def print_header(file):
  print(f"\n{'='*50}")
  print(f"WORD FREQUENCY ANALYSIS - {file}")
  print(f"{'='*50}\n")

# Print statistics about words
def print_stats(counts):
  # VIOLATION 5: Print results mixed with computation
  print(f"Total words (after removing stopwords): {total_words(counts)}")
  print(f"Unique words: {len(counts)}\n")

# Print the top N words
def print_top_n_words(sorted_words, top_n):
  print(f"Top {top_n} most frequent words:\n")

  # VIOLATION 6: Hardcoded formatting
  for i, (word, count) in enumerate(sorted_words[:top_n], 1):
    bar = "*" * count
    print(f"{i:2}. {word:15} {count:3} {bar}")

# Main function coordinating the workflow
def main():
  text = load_file(CONFIG["input_file"])
  stopwords = load_stopwords(CONFIG["stopwards_file"])

  text = normalize(text)
  words = tokenize(text)
  counts = get_counts(words, stopwords, CONFIG["punctuation"])
  sorted_words = sort_counts(counts)

  print_header(CONFIG["input_file"])
  print_stats(counts)
  print_top_n_words(sorted_words, CONFIG["top_n"])
  print()

# Entry point
if __name__ == "__main__":
  main()
