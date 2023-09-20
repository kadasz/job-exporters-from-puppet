#!/usr/bin/env python3

import json
import subprocess

VERSION = '0.0.1a'

def check_targets():
  try:
    p = subprocess.Popen([
      "curl", "-s", "-XGET", "http://prometheus.doamin.com:9090/api/v1/targets" ],
    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    out = json.loads(stdout.decode("utf-8"))
    return [
        v.get('instance') for i in out.get('data')['activeTargets']
        for k,v in i.items() if k == "labels" and v.get('job') == "node" and v.get('instance') != "localhost:9090"
        ]
  except Exception as e:
    print(e)
