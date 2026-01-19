#!/usr/bin/env python3 -B
"""Word frequency counter - the messy version"""

"""
AQ2: Single Responsibility Principle (SRP)
Divided the big function into smaller functions load_file, print_header, get_words, and print_results
"""
def load_file(file):
  with open(file) as f:
    return f.read()
  
def print_header(file):
  print(f"\n{'='*50}")
  print(f"WORD FREQUENCY ANALYSIS - {file}")
  print(f"{'='*50}\n")

def get_words(text):
  words = text.lower().split()
  counts = {}
  stopwords = ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
               "of", "is", "was", "are", "were", "be", "been", "with"]  # Hardcoded!
  
  for word in words:
    # Hardcoded punctuation removal
    word = word.strip('.,!?;:"()[]')
    if word and word not in stopwords:  # Hardcoded stopwords
      counts[word] = counts.get(word, 0) + 1
  
  return counts

def print_results(counts, top_n):
  # VIOLATION 4: Sort and filter inline
  sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
  
  # VIOLATION 5: Print results mixed with computation
  print(f"Total words (after removing stopwords): {sum(counts.values())}")
  print(f"Unique words: {len(counts)}\n")
  print(f"Top {top_n} most frequent words:\n")
  
  # VIOLATION 6: Hardcoded formatting
  for i, (word, count) in enumerate(sorted_words[:top_n], 1):
    bar = "*" * count
    print(f"{i:2}. {word:15} {count:3} {bar}")
  
  print()

# Main function coordinating the workflow
def count_words(file="essay.txt"):

  text = load_file(file)

  print_header(file)
  
  counts = get_words(text)
  
  print_results(counts, 10)

count_words("essay.txt")
