#!/usr/bin/env python

import os, sys
from datetime import date, datetime
import re
import collections

# NETWORK  [thread2] connection accepted from 10.170.39.111:48434 #370521 (17537 connections now open)
connection_accepted_pattern = re.compile( r'NETWORK  \[thread[0-9]+\] connection accepted from ([0-9.]+):([0-9]+) #([0-9]+)' )
# NETWORK  [conn370521] received client metadata from 10.170.39.111:48434 conn370521: { driver: { name: "NetworkInterfaceASIO-Replication", version: "3.4.4" }, os: { type: "Linux", name: "Red Hat Enterprise Linux Server release 7.2 (Maipo)", architecture: "x86_64", version: "Kernel 3.10.0-327.36.3.el7.x86_64" } }
client_metadata_pattern = re.compile( r'NETWORK  \[conn([0-9]+)\] received client metadata from ([0-9.]+):([0-9]+) conn[0-9]+: \{ driver: \{ name: "([\w,-]+)", version: "([0-9.]+)" \}' )
# NETWORK  [replExecDBWorker-0] Skip closing connection for connection # 370521
skip_closing_pattern = re.compile( r'NETWORK  \[replExecDBWorker-[0-9]+\] Skip closing connection for connection # ([0-9]+)' )
# pat = re.compile( r'^(\w+ \d+ \d+:\d+:\d+) ([a-zA-Z0-9\-]+)? ([^:]+): (.+)' )

f = open(sys.argv[1], "r")
connections = {}
missing = []
for line in f:
    if line.find("NETWORK") != -1:
        m = connection_accepted_pattern.search(line)
        if m is not None:
            connections[m.group(3)] = { 'ip':m.group(1), 'port':m.group(2), 'driverName':"None", 'skipped':False }
        else:
            m = client_metadata_pattern.search(line)
            if m is not None:
                conn = connections[m.group(1)]
                conn['driverName'] = m.group(4)
            else:
                m = skip_closing_pattern.search(line)
                if m is not None:
                    if m.group(1) in connections:
                        conn = connections[m.group(1)]
                        conn['skipped'] = True
                    else:
                        missing.append(m.group(1))
f.close()

count = collections.Counter()
for k, v in connections.items():
    if v['skipped']:
        count[v['driverName']] += 1
print count

# for k, v in connections.items():
#     print v

# print "Missing"
# for v in missing:
#     print v

