#!/bin/bash
folder="individual-file-diffs"
file="index.html"

if [ -d "$folder" ]; then 
  rm -r "$folder"
fi

if [ -f "$file" ]; then
  rm "$file"
fi

mkdir "$folder"

python html_diff.py mood_protocol/ redcap_protocol/

python version_diff.py mood_protocol/ redcap_protocol/