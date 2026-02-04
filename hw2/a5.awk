# A5.awk
# Prints rows 1–10 (after header).
# For rows 11+, prints only rows where column 3 is NOT "?".
# Uses `next` as required by the assignment.
# CSV contains spaces after commas, so FS trims whitespace.

BEGIN {
    FS = " *, *"   # comma with optional surrounding spaces
}

NR == 1 {
    print          # print header
    next
}

{
    data++         # count data rows (excluding header)
}

data <= 10 {
    print          # always print first 10 data rows
    next           # do not check conditions below
}

$3 != "?" {
    print          # rows 11+ where column 3 is not "?"
}
