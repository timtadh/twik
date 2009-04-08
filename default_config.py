import sys, os
sys.stderr = sys.stdout
import cgitb; cgitb.enable()
import warnings
warnings.simplefilter('ignore', UserWarning)

FIELDS = ['HOST', 'PORT', 'USER', 'PASSWD', 'DB']
FIELDS.sort()

try:
    f = open('db.conf', 'r')
    s = f.read()
    f.close
except:
    print 'db.conf does not exist'
    print os.getcwd()
    sys.exit(1)

def proc(s):
    s = s.lstrip().rstrip()
    try: 
        if s.isdigit(): s = int(s)
    except: pass
    return s

d = dict([[proc(y) for y in x.split(':')] for x in s.split('\n') 
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
