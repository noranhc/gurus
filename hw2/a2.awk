# A2: Count how many rows belong to each class. Output one line per class.
# to run: gawk -f a2.awk soybean.csv

NR > 1 {
    count[$NF]++
}

END {
    for (class in count) {
        print class, count[class]
    }
}
