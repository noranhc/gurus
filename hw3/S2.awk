BEGIN { FS="," }
NR==1 { for(i=1;i<=NF;i++) hdr[i]=$i; next }
{ for(i=1;i<=NF;i++) if($i=="?") { cols[hdr[i]]=1; rows[NR]=1 } }
END { print "cols:"; for(c in cols) print c; print "rows:"; for(r in rows) print r }
