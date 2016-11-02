#!/usr/bin/env python

import os, sys
from datetime import date, datetime
import re

# change these logs from this:
# Aug 23 07:10:23 ip-172-16-29-73 mongod.27017[771]: [conn986886] query ovrcmain.devices query: { macAddress: "D4:6A:91:01:31:0E", deleted: false } planSummary: IXSCAN { macAddress: 1.0, deleted: 1.0, class: 1.0 } ntoskip:0 nscanned:1 nscannedObjects:1 keyUpdates:0 writeConflicts:0 numYields:1 nreturned:1 reslen:765 locks:{ Global: { acquireCount: { r: 4 } }, Database: { acquireCount: { r: 2 } }, Collection: { acquireCount: { r: 2 } } } 105ms
# to:
# 2016-05-18T15:02:43.412+0000 [initandlisten] dbexit: 

f = open(sys.argv[1], "r")
pat = re.compile( r'^(\w+ \d+ \d+:\d+:\d+) ([a-zA-Z0-9\-]+)? ([^:]+): (.+)' )
for line in f:
    if line.find("mongod") != -1:
        m = pat.match(line)
        dt = datetime.strptime( "2016 " + m.group(1), '%Y %b %d %H:%M:%S' )
        print dt.strftime('%Y-%m-%dT%H:%M:%S') + ".000+0000", m.group(4)

f.close()


