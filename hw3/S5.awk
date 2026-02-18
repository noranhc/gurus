BEGIN { FS="," }
NR==1 { next }
{ if(seen[$0]++) { n++; rows[n]=NR } }
END { print n+0; for(i=1;i<=n;i++) print rows[i] }
