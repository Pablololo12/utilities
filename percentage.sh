#!/bin/bash

i=0

while [ $i -le 100 ];
do
		  e=$((${i}/2))
		  d=0
		  pexit=""
		  while [ $d -lt $e ];
		  do
					 pexit="$pexit"#
					 d=$((${d}+1))
		  done

		  while [ $d -lt 50 ];
		  do
					 pexit="$pexit"" "
					 d=$((${d}+1))
		  done
		  
		  echo -en '\r['"$pexit""]$i%"
		  i=$((${i}+1))
		  sleep 0.2
done

echo ""
