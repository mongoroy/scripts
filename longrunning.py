#!/usr/bin/python

import sys

testFile = open(sys.argv[1], "r")
time = int(sys.argv[2])

for line in testFile:
    if line.endswith("ms\n") and int(line.split()[-1][:-2]) > time:
        sys.stdout.write( line )
