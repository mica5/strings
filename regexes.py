#!/usr/bin/env python
import re

# find lines that are indented by a number of spaces that isn't a multiple of 4
indentation_not_multiple_of_4_1 = re.compile(
    r'^( {4})*( {1,3})(?![\S ])'
)
indentation_not_multiple_of_4_2 = re.compile(
    r'^( {4})*( {1,3})(?![^a-zA-Z\n0-9}])'
)
