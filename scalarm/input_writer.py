#!/usr/bin/env python2.6
import json, sys
 
data = None
with open(sys.argv[1]) as json_data:
    data = json.load(json_data)
 
ants = data['ants']
iterations = data['iterations']
city = data['city']
ptype = data['ptype']
egocentric = data['egocentric']
altercentric = data['altercentric']
goodConflict = data['goodConflict']
badConflict = data['badConflict']
name = data['name']
 
with open('input.txt', 'wb+') as f:
    f.write("%s %s %s %s %s %s %s %s %s" % (ants, iterations, city, ptype, egocentric, altercentric, goodConflict, badConflict, name))