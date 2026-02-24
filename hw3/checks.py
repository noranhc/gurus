import csv
import sys

MISSING = '?'

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

#--- Presentation Layer ---

def print_results(check, results):
    print(f'Check {check}')
    for item in results:
        print(item)

def print_check_d_results(bad_cols):
    print_results('D: Conflicting Features', bad_cols)

def print_check_e_results(bad_cols):
    print_results('E: Implausible Features', bad_cols)

#--- Entry Point ---

CHECKS = {
    'd': check_d,
    'e': check_e,
}

if __name__ == '__main__':
    target = sys.argv[1].lower()
    path = sys.argv[2]
    CHECKS[target](path)
