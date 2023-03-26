"""
Convert the below command into python script.
nomad job inspect hello-world | jq '.Job.TaskGroups[0].Count = 1' | nomad job run -json -
"""

import json
import requests

import urllib3
from urllib3 import exceptions
from rich.pretty import pprint as print

urllib3.disable_warnings(exceptions.InsecureRequestWarning)

job_name = "hello-world"
base_url = "https://localhost:4646"
verify   = False

# Get the current job spec
resp = requests.get(base_url + f"/v1/job/{job_name}", verify=verify)
job_spec = json.loads(resp.text)

# Modify the job spec
job_spec["TaskGroups"][0]["Count"] = 2
print(job_spec)

# Submit the modified job spec
headers = {"Content-Type": "application/json"}
resp = requests.post(
    base_url + f"/v1/job/{job_name}",
    headers=headers,
    data=json.dumps({"Job": job_spec}),
    verify=verify,
)

print(resp.text)
print(resp)
