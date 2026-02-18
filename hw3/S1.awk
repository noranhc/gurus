BEGIN { FS="," }
NR==1 { ncols=NF; next }
NF != ncols { n++; print NR }
END { print n+0 > "/dev/stderr" }
