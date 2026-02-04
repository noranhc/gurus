# A6: Write a function entropy(arr, n) and print the entropy of the
# class distribution
# Formula: -sum(p * log(p)) where p = count/n

BEGIN { FS =","; n=0 }

# Skip header
NR==1 { next }

# Count each class
{
    counts[$NF]++
    n++
}

# Entropy function: arr holds counts, n is total
function entropy(arr, n,    c, p, e) {
    e = 0
    for (c in arr) {
        p = arr[c] / n
        if (p > 0)
            e -= p * log(p)
    }

    return e
}

END {
    e = entropy(counts, n)
    printf "Class distribution entropy: %.4f\n", e

    # Class counts for reference
    print "\nClass counts:"
    for (c in counts)
        printf "%s: %d\n", c, counts[c]

    printf "\nTotal rows: %d\n", n
}
