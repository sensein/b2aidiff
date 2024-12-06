#!/bin/bash

mkdir individual-file-diffs

python html_diff.py /path/to/mood/protocol /path/to/redcap/protocol

python version_diff.py /path/to/mood/protocol /path/to/redcap/protocol