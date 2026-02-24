# Checks for HW3
# Usage: python3 checks.py [check] [filename]
# Example: python3 checks.py A page_blocks_dirty.csv

import csv
import sys
from math import sqrt

#--- Model Layer (Business logic, no I/O) ---

# Shared utilities

def mean(xs):
    return sum(xs) / len(xs)

def sd(xs):
    mu = mean(xs)
    return sqrt(sum((x - mu)**2 for x in xs) / len(xs))

# QA. Identical features 
# Identify columns with the same values for every row.
# Report all columns in each identical group.

def find_identical_features(data, header):
    identical_groups = []
    for i in range(len(header)):
        group = [header[i]]
        for j in range(i + 1, len(header)):
            if all(row[i] == row[j] for row in data):
                group.append(header[j])
        if len(group) > 1:
            identical_groups.append(group)
    return identical_groups

def check_a(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    identical_groups = find_identical_features(data, header)
    print_check_a_results(identical_groups)

# QB. Correlated features
# Count correlated pairs of numeric features with Pearson |r| > 0.95.
# Report both column names in each pair.

def pearson(xs, ys):
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx  = sum((x - mx)**2 for x in xs)
    dy  = sum((y - my)**2 for y in ys)
    if dx == 0 or dy == 0:
        return 0
    return num / sqrt(dx * dy)

def is_numeric_column(data, col_idx):
    try:
        for row in data:
            float(row[col_idx])
        return True
    except (ValueError, IndexError):
        return False
    
def get_numeric_cols(data, header):
    numeric_cols = []
    for i in range(len(header)):
        if is_numeric_column(data, i) and not header[i].endswith('!'):
            numeric_cols.append(i)
    return numeric_cols

def check_correlation(xs, ys):
    r = pearson(xs, ys)
    return abs(r) > 0.95

def find_correlated_pairs(data, header):
    numeric_cols = get_numeric_cols(data, header)
    correlated_pairs = []
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            xs = [float(row[numeric_cols[i]]) for row in data]
            ys = [float(row[numeric_cols[j]]) for row in data]
            if check_correlation(xs, ys):
                correlated_pairs.append((header[numeric_cols[i]], header[numeric_cols[j]]))
    return correlated_pairs

def check_b(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)
    
    correlated_pairs = find_correlated_pairs(data, header)
    print_check_b_results(correlated_pairs)

# QC. Outlier features
# Columns that contain at least one value more than 3 standard deviations
# from the column mean (μ ± 3σ).

def has_outliers(xs):
    mu = mean(xs)
    sigma = sd(xs)
    threshold = 3 * sigma
    
    for x in xs:
        if abs(x - mu) > threshold:
            return True
    return False

def find_outlier_features(data, header):
    numeric_cols = get_numeric_cols(data, header)
    outlier_cols = []
    
    for col_idx in numeric_cols:
        xs = [float(row[col_idx]) for row in data]
        if has_outliers(xs):
            outlier_cols.append(header[col_idx])
    
    return outlier_cols

def check_c(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)
    
    outlier_cols = find_outlier_features(data, header)
    print_check_c_results(outlier_cols)

#--- Presentation Layer ---

def print_results(check, results):
    print(f'Check {check}')
    for item in results:
        print(item)

def print_check_a_results(identical_groups):
    print_results('A: Identical Features', [','.join(group) for group in identical_groups])

def print_check_b_results(correlated_pairs):
    print_results('B: Correlated Features', [f'{col1},{col2}' for col1, col2 in correlated_pairs])

def print_check_c_results(outlier_cols):
    print_results('C: Outlier Features', outlier_cols)

#--- Program entry point ---

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 checks.py [check] [filename]")
        print("Example: python3 checks.py A page_blocks_dirty.csv")
        sys.exit(1)
    
    check = sys.argv[1].upper()
    filename = sys.argv[2]
    
    if check == 'A':
        check_a(filename)
    elif check == 'B':
        check_b(filename)
    elif check == 'C':
        check_c(filename)
    elif check == 'D':
        print(f"Check {check} not yet implemented")
    else:
        print(f"Unknown check: {check}")


if __name__ == "__main__": main()
