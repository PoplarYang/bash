#!/bin/bash

from_type=$1
to_type=$2
watch_dir=$3
dest_dir=$4
inotifywait -rme create $watch_dir --format '%f' | while read line; do
	echo "$line"
	if [[ "$line" == *.${from_type} ]]; then
		filename=$(echo "$line" | cut -d'.' -f 1 )
		/usr/bin/convert $watch_dir/"$line" $dest_dir/${filename}.${to_type}
	fi
done
