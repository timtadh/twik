import sys
sys.stderr = sys.stdout
import cgitb; cgitb.enable()
import warnings
warnings.simplefilter('ignore', UserWarning)

FIELDS = ['HOST', 'PORT', 'USER', 'PASSWD', 'DB']
FIELDS.sort()

f = open('db.conf', 'r')
s = f.read()
f.close

d = dict([[y.lstrip().rstrip() for y in x.split(':')] for x in s.split('\n')
                                        if x and x.lstrip()[0] != '#' and len(x.split(':')) == 2])
keys = d.keys()
keys.sort()

try:
    assert keys == FIELDS
except AssertionError, e: 
    print '''You database file does not match the schema:
        HOST:host
        PORT:3306
        USER:user
        PASSWD:password
        DB:database'''
    print 'yours -> \n', s

import db
for k in keys:
    db.__setattr__(k, d[k])
