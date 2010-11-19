#!/usr/bin/env python
# coding=utf-8

import sys
import os

f = open( sys.argv[1], 'a+')

f.write( "%f: " + sys.argv[1] + "\n" )
f.write( "%d: " + sys.argv[2] + "\n" )
f.write( "%s: " + sys.argv[3] + "\n" )
f.write( "%n: " + sys.argv[4] + "\n" )
f.write( "%D: " + sys.argv[5] + "\n" )
f.write( "%t: " + sys.argv[6] + "\n" )

f.close()

