# A3: Compute the most common value in column 2. Print the value and its count.
# to run: gawk -f a3.awk soybean.csv

NR > 1 {
    count[$2]++
}

END {
    max_count = 0
    max_value = ""
    for (value in count) {
        if (count[value] > max_count) {
            max_count = count[value]
            max_value = value
        }
    }
    print max_value, max_count
}
