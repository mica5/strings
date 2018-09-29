#!/usr/bin/env bash

this_dir="$(dirname "$(readlink -e "$0")")"

cat <<EOF | "$this_dir"/indented_text_to_html_list.py
Main level item 1
    Indented level item 1
    Indented level item 2
        Double-indented level item 1
Main level item 2
EOF
