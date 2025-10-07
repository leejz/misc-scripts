#!/bin/bash python
import json
import yaml
import sys
json_fn = sys.argv[1]
print("The JSON string file is:", json_fn)
with open(json_fn, 'r') as fh:
  json_string=''.join([line.strip() for line in fh.readlines()])
python_dict=json.loads(json_string)
yaml_string=yaml.dump(python_dict)
outfile=json_fn + '.yaml'
print("The YAML string file is:", outfile)
with open(outfile, 'w') as fh:
  for line in yaml_string:
    fh.write(line)
