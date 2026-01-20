#!/usr/bin/env python3 -B
"""Word frequency counter - the messy version"""

"""
AQ1: Separation of Concerns (SoC)
Separated the code into Model and Presentation layers.

AQ2: Single Responsibility Principle (SRP)
Divided the big function into smaller functions
< 10 lines of code each and responsible for a single task.
"""

#--- MODEL LAYER (Pure business logic, no I/O) ---

# Load file content
def load_file(file):
  with open(file) as f:
    return f.read()

# Load stopwords
def load_stopwords(file):
  with open(file) as f:
    return set(line.strip() for line in f)

# Q4: Small Functions violation:
#     get_counts() performs multiple steps (cleaning + filtering + counting).
# AQ4: Fix (step 1):
#     Extract word cleaning into a small obvious function.
def clean_word(word):
  return word.strip('.,!?;:"()[]')

# Q4: Small Functions violation:
#     get_counts() performs multiple steps (cleaning + filtering + counting).
# AQ4: Fix (step 2):
#     Extract filtering into a small obvious function.
def valid_word(word, stopwords):
  return bool(word) and word not in stopwords

# Process text to get word counts
def get_counts(text):
  words = text.lower().split()
  counts = {}
  stopwords = load_stopwords("stopwords.txt")
  for word in words:
    # Hardcoded punctuation removal
    word = clean_word(word)
    if valid_word(word, stopwords):  # Hardcoded stopwords
      counts[word] = counts.get(word, 0) + 1
  return counts

#--- PRESENTATION LAYER (I/O only, no logic) ---

# Print header
def print_header(file):
  print(f"\n{'='*50}")
  print(f"WORD FREQUENCY ANALYSIS - {file}")
  print(f"{'='*50}\n")

# Print statistics about words
def print_stats(counts, n, top_n):
  # VIOLATION 5: Print results mixed with computation
  print(f"Total words (after removing stopwords): {n}")
  print(f"Unique words: {len(counts)}\n")

# Print the top N words
def print_top_n_words(sorted_words, top_n):
  print(f"Top {top_n} most frequent words:\n")

  # VIOLATION 6: Hardcoded formatting
  for i, (word, count) in enumerate(sorted_words[:top_n], 1):
    bar = "*" * count
    print(f"{i:2}. {word:15} {count:3} {bar}")

# Main function coordinating the workflow
def count_words(file="essay.txt"):
  text = load_file(file)
  counts = get_counts(text)
  n = sum(counts.values())
  sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
  top_n = 10  # Hardcoded!

  print_header(file)
  print_stats(counts, n, top_n)
  print_top_n_words(sorted_words, top_n)
  print()

count_words("essay.txt")
