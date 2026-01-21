#!/usr/bin/env python3 -B

import json

"""Word frequency counter - the messy version"""

"""
AQ1: Separation of Concerns (SoC)
Separated the code into Model and Presentation layers.

AQ2: Single Responsibility Principle (SRP)
Divided the big function into smaller functions
< 10 lines of code each and responsible for a single task.

AQ3: Mechanism vs Policy
Hardcode punctuation and stopword rules were were moved
into CONFIG and passed into pure functions.
"""

CONFIG = {
  "input_file": "essay.txt",
  "punctuation": '.,!?;:"()[]',
  "top_n": 10,
  "bar_char": "*",
  "word_width": 15,
  "language": "english", # english | spanish (bonus 4)
  "stopwords_file": { # 2D list that requires language as key to access file (bonus 4)
      "english": "stopwords.txt",
      "complete": "stopwords_complete.txt",
      "spanish": "stopwords_es.txt"
  },
  "output_format": "csv", # json | csv (bonus 1)
  "output_file": "output"
}

#--- MODEL LAYER (Pure business logic, no I/O) ---

# Load file content
def load_file(file):
  with open(file) as f:
    return f.read()

# Bonus Task 1
# Write file content
def write_file(path, content):
  with open(path, 'w') as f:
    f.write(content)

# Load stopwords
def load_stopwords(file):
  with open(file) as f:
    return set(line.strip() for line in f)

# Process text to get list of words
def process_text(text):
  text = text.lower()
  return text.split()

# Process words to get counts
def get_counts(words, stopwords, punctuation):
  counts = {}
  for word in words:
    word = word.strip(punctuation)
    if bool(word) and word not in stopwords:
      counts[word] = counts.get(word, 0) + 1
  return counts

# Sorts list based on counts
def sort_counts(counts):
  return sorted(counts.items(), key=lambda x: x[1], reverse=True)

# Returns the total number of words in text
def total_words(counts):
  return sum(counts.values())

# Bonus Task 1
# Write Bonus Output to file
# Dynamically builds output file name based on output format
def write_bonus_output(result):
  if CONFIG["output_format"] == "json":
    write_file(CONFIG["output_file"] + f".{CONFIG['output_format']}", toJSON(result))
  elif CONFIG["output_format"] == "csv":
    write_file(CONFIG["output_file"] + f".{CONFIG['output_format']}", toCSV(result))

#--- PRESENTATION LAYER (I/O only, no logic) ---

# Print header
def print_header(file):
  print(f"\n{'='*50}")
  print(f"WORD FREQUENCY ANALYSIS - {file}")
  print(f"{'='*50}\n")

# Print statistics about words
def print_stats(counts):
  print(f"Total words (after removing stopwords): {total_words(counts)}")
  print(f"Unique words: {len(counts)}\n")

# Print the top N words
def print_top_n_words(sorted_words, top_n, bar_char, width):
  print(f"Top {top_n} most frequent words:\n")

  for i, (word, count) in enumerate(sorted_words[:top_n], 1):
    bar = bar_char * count
    print(f"{i:2}. {word:{width}} {count:3} {bar}")

# Bonus Task 1
# Build JSON object
def toJSON(result):
  return json.dumps(result, indent=2)

# Bonus Task 1
# Build CSV string
def toCSV(result):
  lines = ["word,count"]
  for word, count in result["top"]:
    lines.append(f"{word},{count}")
  return "\n".join(lines)

# Bonus Task 1
# Build result dictionary
def build_result(counts, sorted_words, top_n):
  return {
    "total": total_words(counts),
    "unique": len(counts),
    "counts": counts,
    "top": sorted_words[:top_n]
  }

def output_result(counts, sorted_words):
  print_header(CONFIG["input_file"])
  print_stats(counts)
  print_top_n_words(sorted_words, CONFIG["top_n"], CONFIG["bar_char"], CONFIG["word_width"])
  print()

  result = build_result(counts, sorted_words, CONFIG["top_n"])
  write_bonus_output(result)

# Main function coordinating the workflow
def main():
  text = load_file(CONFIG["input_file"])
  stopwords = load_stopwords(CONFIG["stopwords_file"][CONFIG["language"]])

  words = process_text(text)
  counts = get_counts(words, stopwords, CONFIG["punctuation"])
  sorted_words = sort_counts(counts)

  output_result(counts, sorted_words)

# Entry point
if __name__ == "__main__":
  main()
