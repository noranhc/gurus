# a5.awk
# Prints rows 1–10
# For rows 11+, print only rows where column 3 is NOT "?".
# Uses "next"

BEGIN {
    FS=","          # Set field separator to comma for CSV
}

NR == 1 {
    print           # Always print the header row
    next            # Skip further processing for header
}

{
    data++          # Count number of data rows (excluding header)
}

data <= 10 {
    print           # Print the first 10 data rows
    next            # Skip further checks for these rows
}

$3 != "?" {
    print           # For remaining rows, print only if column 3 is not "?"
}
