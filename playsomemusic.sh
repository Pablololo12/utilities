#!/bin/ksh

exec 2>/dev/null
TMPFILE=".temporal_file"
URL=""
urls=()
titles=()

handler()
{
    rm $TMPFILE
    exit
}

trap handler SIGINT

mpv >/dev/null
if [ "$?" -ne 0 ]; then
	echo "MPV is needed"
	exit
fi

if [ "$#" = 0 ]; then
	echo -n "Insert URL: "
	read URL
else
	URL="$1"
fi

curl -s "$URL" -o $TMPFILE
if [ "$?" -ne 0 ]; then
	echo "Bad URL"
	exit
fi

i=0
grep -o -e "https://www.youtube.com/watch?v=..........." $TMPFILE | sort -u | while read url; do
  urls[$i]="$url"
  #echo $url
  ((i++))
done

grep -o -e "data-video-id=............." $TMPFILE | grep -o -e "\"...........\"" | while read url; do
  urls[$i]="http://www.youtube.com/watch?v=${url:1:11}"
  #echo ${urls[$i]}
  ((i++))
done

size="$i"

i=0
grep -o -e "data-title=\"[^\"]*\"" $TMPFILE | cut -d "\"" -f 2 | while read title; do
  titles[$i]=$title
  #echo $title
  ((i++))
done

echo Controls:
echo space: play/pause
echo arrows to advance
echo q: quit song and play the next one
echo 

i=0
while true; do
	echo
	echo "Playing ${titles[$i]}"
	mpv "${urls[$i]}" --no-video --quiet
	((i++))
	if [ "$i" = "$size" ]; then
		i=0;
	fi
done

rm $TMPFILE