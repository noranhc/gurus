BEGIN { FS="," }
NR==1 { for(i=1;i<=NF;i++) hdr[i]=$i; next }
NR==2 { for(i=1;i<=NF;i++) first[i]=$i }
NR>2  { for(i=1;i<=NF;i++) if($i!=first[i]) bad[i]=1 }
END { n=0; for(i=1;i<=length(hdr);i++) if(!(i in bad)) { n++; print hdr[i] } }
