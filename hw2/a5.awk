BEGIN { FS="," }
NR==1 { print; next }
{ data++ }
data <= 10 { print; next }
$3 != "?" { print }    #print only rows where column 3 is not "?"
