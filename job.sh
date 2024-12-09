#!/bin/bash
folder="individual-file-diffs"
file="diff.html"

rm "$folder"
mkdir "$folder"
rm "$file"

python html_diff.py mood_protocol/ redcap_protocol/

python version_diff.py mood_protocol/ redcap_protocol/