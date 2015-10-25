#!/usr/bin/env python2.6
import json, os
 
with open('output.txt', 'r') as f:
    output = f.read()
 
try:
    result = float(output)
    results = { "status": "ok", "results": { "fitness": output } }
except ValueError:
    results = { "status": "error", "reason": output }
 
with open('output.json', 'wb+') as f:
    f.write(json.dumps(results))