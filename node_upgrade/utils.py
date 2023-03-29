import json
import requests

job_name = "hello-world"
base_url = "https://localhost:4646"
verify   = False

import urllib3
from urllib3 import exceptions
urllib3.disable_warnings(exceptions.InsecureRequestWarning)

def get_job_spec(job_name):
    resp = requests.get(base_url + f"/v1/job/{job_name}", verify=verify)
    job_spec = json.loads(resp.text)
    return job_spec

def update_count(count, job_spec):
    job_spec["TaskGroups"][0]["Count"] = count
    return job_spec

def short_id(id):
    return id[:8]

def print_json(dict):
    json_string = json.dumps(dict, indent=2)
    print(json_string)

def write_json_to_file(dict, filename):
    with open(filename, "w") as f:
        json.dump(dict, f, indent=2)

def confirm(message, action):
    """ Ask for confirmation before action. """
    print(message)
    if input("y/n: ") == "y":
        action()
        return True
    return False

def noop():
    """ A no op function """
    pass

