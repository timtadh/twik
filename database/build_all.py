#!/bin/python

import os, sys
cwd = os.getcwd()
os.chdir('..')
sys.path.append(os.getcwd())
import templater
os.chdir(cwd)

SRC_DIR = 'src'
BUILD_DIR = 'build'
CREATE_DIR = 'create'
TABLE_CREATE_FILE = 'create_tables.sql'

DATABASE = 'diplomacy'

src_files = os.listdir(SRC_DIR)

for name in src_files:
    in_path = os.sep.join((SRC_DIR, name))
    out_path = os.sep.join((BUILD_DIR, name))
    out_f = open(out_path, 'w')
    
    templater.print_template(in_path, locals(), out_f)
    
    out_f.close()
