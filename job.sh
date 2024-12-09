#!/bin/bash
folder="individual-file-diffs"
file="diff.html"

if [ -d "/path/to/folder" ]; then
  rm "$folder"
fi

if [ -f "/path/to/file" ]; then
  rm "$file"
fi

mkdir "$folder"

python html_diff.py mood_protocol/ redcap_protocol/

python version_diff.py mood_protocol/ redcap_protocol/