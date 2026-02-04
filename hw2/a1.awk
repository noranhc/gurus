# A1: Print every line where the class (last column) is diaporthe-stem-canker.
# to run: gawk -f a1.awk soybean.csv

$NF == "diaporthe-stem-canker"
