# Checks for HW3
# Usage: python3 checks.py [check] [filename]
# Example: python3 checks.py A page_blocks_dirty.csv

import csv
import sys
from math import sqrt

MISSING = '?'

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

# QD. Features with conflicting values
# Columns involved in ≥1 violated referential integrity constraint.
# Checks: AREA=H*L, ECCEN=L/H (tol 0.01),
# P_BLACK=BLACKPIX/AREA, P_AND=BLACKAND/AREA (tol 0.001).

INTEGRITY_FIELDS = [
    'HEIGHT','LENGHT','AREA','ECCEN',
    'P_BLACK','P_AND','BLACKPIX','BLACKAND'
]

def has_missing(row, fields):
    return any(row[c] == MISSING for c in fields)

def integrity_violations(row):
    h  = float(row['HEIGHT'])
    l  = float(row['LENGHT'])
    a  = float(row['AREA'])
    e  = float(row['ECCEN'])
    pb = float(row['P_BLACK'])
    pa = float(row['P_AND'])
    bpx = float(row['BLACKPIX'])
    ba = float(row['BLACKAND'])

    cols = set()
    if a != h * l:
        cols.update(['AREA', 'HEIGHT', 'LENGHT'])
    if h > 0 and abs(e - l / h) > 0.01:
        cols.update(['ECCEN', 'LENGHT', 'HEIGHT'])
    if a > 0 and abs(pb - bpx / a) > 0.001:
        cols.update(['P_BLACK', 'BLACKPIX', 'AREA'])
    if a > 0 and abs(pa - ba / a) > 0.001:
        cols.update(['P_AND', 'BLACKAND', 'AREA'])
    return cols

def find_conflicting_features(rows):
    bad_cols = set()
    for r in rows:
        if has_missing(r, INTEGRITY_FIELDS):
            continue
        bad_cols.update(integrity_violations(r))
    return sorted(bad_cols)

def check_d(filename):
    with open(filename) as f:
        rows = list(csv.DictReader(f))
    bad_cols = find_conflicting_features(rows)
    print_check_d_results(bad_cols)

# QE. Features with implausible values
# Columns with ≥1 value violating a plausibility constraint.
# Checks: positive values, proportions in [0,1],
# BLACKPIX <= BLACKAND, class! in {1..5}.

POS_COLS = [
    'HEIGHT','LENGHT','WIDTH','AREA',
    'BLACKPIX','BLACKAND','WB_TRANS','MEAN_TR','ECCEN'
]
PROP_COLS = ['P_BLACK', 'P_AND']
VALID_CLASSES = {'1','2','3','4','5'}
def check_positive(row):
    cols = set()
    for c in POS_COLS:
        if row[c] != MISSING and float(row[c]) <= 0:
            cols.add(c)
    return cols

def check_proportions(row):
    cols = set()
    for c in PROP_COLS:
        if row[c] != MISSING:
            v = float(row[c])
            if v < 0 or v > 1:
                cols.add(c)
    return cols

def check_blackpix_subset(row):
    if (row['BLACKPIX'] != MISSING
            and row['BLACKAND'] != MISSING
            and float(row['BLACKPIX']) > float(row['BLACKAND'])):
        return {'BLACKPIX', 'BLACKAND'}
    return set()


def plausibility_violations(row):
    return (check_positive(row)
          | check_proportions(row)
          | check_blackpix_subset(row))

def find_implausible_features(rows):
    bad_cols = set()
    for r in rows:
        bad_cols.update(plausibility_violations(r))
    return sorted(bad_cols)

def check_e(filename):
    with open(filename) as f:
        rows = list(csv.DictReader(f))
    bad_cols = find_implausible_features(rows)
    print_check_e_results(bad_cols)

# QG. Outlier cases
# Rows containing at least one value more than 3σ from
# the column mean. Row-level dual of check C.

def column_stats(rows, header):
    """Compute mean and sd for each numeric column."""
    stats = {}
    for col in header:
        vals = []
        for r in rows:
            if r[col] != MISSING:
                try:
                    vals.append(float(r[col]))
                except ValueError:
                    break
        else:
            if vals:
                stats[col] = (mean(vals), sd(vals))
    return stats

def is_outlier_row(row, stats):
    """True if any value is more than 3σ from column mean."""
    for col, (mu, sigma) in stats.items():
        if row[col] == MISSING:
            continue
        if sigma > 0 and abs(float(row[col]) - mu) > 3 * sigma:
            return True
    return False

def find_outlier_cases(rows, header):
    stats = column_stats(rows, header)
    bad_rows = []
    for i, r in enumerate(rows):
        if is_outlier_row(r, stats):
            bad_rows.append(i + 2)
    return bad_rows

def check_g(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)
    bad_rows = find_outlier_cases(rows, header)
    print_check_g_results(bad_rows)

#--- Presentation Layer ---

def print_results(check, results):
    print(f'Check {check} - {len(results)}')
    for item in results:
        print(item)

def print_check_a_results(identical_groups):
    print_results('A: Identical Features', [','.join(group) for group in identical_groups])

def print_check_b_results(correlated_pairs):
    print_results('B: Correlated Features', [f'{col1},{col2}' for col1, col2 in correlated_pairs])

def print_check_c_results(outlier_cols):
    print_results('C: Outlier Features', outlier_cols)

def print_check_d_results(bad_cols):
    print_results('D: Conflicting Features', bad_cols)

def print_check_e_results(bad_cols):
    print_results('E: Implausible Features', bad_cols)

def print_check_g_results(bad_rows):
    print_results('G: Outlier Cases', bad_rows)

#--- Program entry point and execution ---

CHECKS = {
    'a': check_a,
    'b': check_b,
    'c': check_c,
    'd': check_d,
    'e': check_e,
    'g': check_g,
}

def run_check(check_name, filename):
    check_func = CHECKS.get(check_name.lower())
    if check_func:
        check_func(filename)
    else:
        print(f"Unknown check: {check_name}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 checks.py [check] [filename]")
        print("Example: python3 checks.py A page_blocks_dirty.csv")
        sys.exit(1)

    check_name = sys.argv[1]
    filename = sys.argv[2]

    run_check(check_name, filename)

if __name__ == "__main__":
    main()
