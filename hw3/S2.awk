BEGIN { FS="," }
NR==1 { for(i=1;i<=NF;i++) hdr[i]=$i; next }
{ for(i=1;i<=NF;i++) if($i=="?") { cols[hdr[i]]=1; rows[NR]=1 } }
END { for(c in cols) print c; for(r in rows) print r }
