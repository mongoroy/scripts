# scripts

collection of ad-hoc scripts made to handle mongodb support situations

## longrunning.py

will print out lines from a mongod log that took longer than the specified number of ms

to run: longrunning.py [mongod log] [min time in ms]

## syslog-to-mongodlog.py

will transform syslog mongod lines to mongod log format

to run: syslog-to-mongodlog.py [syslog]

