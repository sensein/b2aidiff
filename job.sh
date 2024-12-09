#!/bin/bash
name="individual-file-diffs"
file="diff.html"

rm "$dir_name"
mkdir "$dir_name"
rm "$file"

python html_diff.py mood_protocol/ redcap_protocol/

python version_diff.py mood_protocol/ redcap_protocol/