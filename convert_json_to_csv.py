#!/bin/bash python3

import json
import sys
json_fn=sys.argv[1]
json_key=sys.argv[2] #predicted_aligned_error
out_fn=json_fn + '.csv'
print('infile:' + json_fn)
with open(json_fn, 'r') as fh:
  json_string=''.join([line.strip() for line in fh.readlines()])
python_dict=json.loads(json_string)
mat=python_dict[json_key]

print('outfile:' + out_fn)
with open(out_fn,'w') as fh:
    for line in mat:
        fh.write(','.join([str(c) for c in line])+'\n')

