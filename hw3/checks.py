import csv, sys

MISSING = '?'

def check_D(path):
    """Columns in ≥1 violated referential integrity."""
    with open(path) as f:
        rows = list(csv.DictReader(f))

    bad_cols = set()
    needed = ['HEIGHT','LENGHT','AREA','ECCEN','P_BLACK','P_AND','BLACKPIX','BLACKAND']

    for r in rows:
        if any(r[c] == MISSING for c in needed):
            continue
        h = float(r['HEIGHT']); l = float(r['LENGHT'])
        a = float(r['AREA']);   e = float(r['ECCEN'])
        pb = float(r['P_BLACK']); pa = float(r['P_AND'])
        bpx = float(r['BLACKPIX']); ba = float(r['BLACKAND'])

        # AREA = HEIGHT * LENGHT
        if a != h * l:
            bad_cols.update(['AREA', 'HEIGHT', 'LENGHT'])
        # ECCEN = LENGHT / HEIGHT
        if h > 0 and abs(e - l / h) > 0.01:
            bad_cols.update(['ECCEN', 'LENGHT', 'HEIGHT'])
        # P_BLACK = BLACKPIX / AREA
        if a > 0 and abs(pb - bpx / a) > 0.001:
            bad_cols.update(['P_BLACK', 'BLACKPIX', 'AREA'])
        # P_AND = BLACKAND / AREA
        if a > 0 and abs(pa - ba / a) > 0.001:
            bad_cols.update(['P_AND', 'BLACKAND', 'AREA'])

    print(len(bad_cols))
    for c in sorted(bad_cols):
        print(c)


def check_E(path):
    """Columns with ≥1 plausibility violation."""
    with open(path) as f:
        rows = list(csv.DictReader(f))

    bad_cols = set()

    # Columns that must be > 0
    pos_cols = ['HEIGHT','LENGHT','WIDTH','AREA','BLACKPIX','BLACKAND','WB_TRANS','MEAN_TR','ECCEN']
    # Columns that must be in [0, 1]
    prop_cols = ['P_BLACK', 'P_AND']

    for r in rows:
        # Check > 0 constraints
        for c in pos_cols:
            if r[c] == MISSING:
                continue
            if float(r[c]) <= 0:
                bad_cols.add(c)

        # Check [0,1] constraints
        for c in prop_cols:
            if r[c] == MISSING:
                continue
            v = float(r[c])
            if v < 0 or v > 1:
                bad_cols.add(c)

        # BLACKPIX <= BLACKAND
        if r['BLACKPIX'] != MISSING and r['BLACKAND'] != MISSING:
            if float(r['BLACKPIX']) > float(r['BLACKAND']):
                bad_cols.update(['BLACKPIX', 'BLACKAND'])

        # class! must be in {1,2,3,4,5}
        cls = r['class!']
        if cls == MISSING or cls.strip() not in ('1','2','3','4','5'):
            bad_cols.add('class!')

    print(len(bad_cols))
    for c in sorted(bad_cols):
        print(c)

if __name__ == '__main__':
    target = sys.argv[1]
    path = sys.argv[2]
    globals()[f'check_{target}'](path)
