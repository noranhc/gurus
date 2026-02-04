# A5.awk
# Print rows 1–10 of the dataset (after the header).
# For rows 11+, print only rows where column 3 is NOT "?".
# Uses `next` as required.

BEGIN {
    FS = " *, *"          # comma with optional surrounding spaces
}

NR == 1 {
    print                 # print header row
    next
}

{
    data++                # count data rows (excluding header)
}

# Always print the first 10 data rows
data <= 10 {
    print
    next                  # do not process further conditions
}

# For rows after the first 10, print only if column 3 is not "?"
data > 10 && $3 != "?" {
    print
}
