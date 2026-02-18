BEGIN { FS="," }
NR==1 { ncols=NF; next }
NF != ncols { n++; rows[n]=NR }
END { print n+0; for(i=1;i<=n;i++) print rows[i] }
