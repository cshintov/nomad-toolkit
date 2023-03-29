"""
Functions for job management.
"""

import json
import requests
import urllib3
from urllib3 import exceptions
from rich.pretty import pprint as print

from utils import *

urllib3.disable_warnings(exceptions.InsecureRequestWarning)

NOMAD_URL = "https://localhost:4646"
VERIFY   = False

def update_job(job_name, job_spec):
    """Submit the modified job spec"""

    headers = {"Content-Type": "application/json"}
    resp = requests.post(
        NOMAD_URL + f"/v1/job/{job_name}",
        headers=headers,
        data=json.dumps({"Job": job_spec}),
        verify=VERIFY,
    )
    return resp

def show_changes_to_be_applied(current_spec):
    print(current_spec["TaskGroups"][0]["Tasks"][0]["Name"])
    print(current_spec["TaskGroups"][0]["Constraints"])
    print(current_spec["TaskGroups"][0]["Tasks"][0]["Config"]["image"])

    print(current_spec["TaskGroups"][1]["Count"])
    print(current_spec["TaskGroups"][1]["Constraints"])
    print(current_spec["TaskGroups"][1]["Tasks"][0]["Name"])
    print(current_spec["TaskGroups"][1]["Tasks"][0]["Config"]["image"])

def deploy(job, current_spec):
    """ Ask for confirmation before updating the job spec. """
    if input("y/n: ") == "y":
        resp = update_job(job, current_spec)
        print(resp.text)
        print(resp.status_code)
        return True
    return False

def get_canary_constraint(canary_group, node):
    """ If there is an existing canary group, get the constraint by looking
    for `set_contains_any` operator. If not found, create a new `constraint`.
    """
    constraints = canary_group.get("Constraints", [])
    for constraint in constraints:
        if constraint["Operand"] == "set_contains_any":
            return constraint

    return {
        "LTarget": "${node.unique.name}",
        "Operand": "set_contains_any",
        "RTarget": node,
    }

def get_allocations(job_name):
    """ Get allocations of the job """
    resp = requests.get(NOMAD_URL + f"/v1/job/{job_name}/allocations", verify=VERIFY)

    # Print the allocation ids and nodes (names) they are running on
    return [(
        alloc["NodeName"],
        short_id(alloc["ID"]),
        alloc['ClientStatus']) for alloc in json.loads(resp.text)]

def scale_up(job_spec):
    count = job_spec["TaskGroups"][0]["Count"]
    update_count(count + 1, job_spec)

def scale_down(job_spec):
    count = job_spec["TaskGroups"][0]["Count"]
    update_count(count - 1, job_spec)

def ask_which_node_to_scale_down(allocs):
    node_to_scale_down = "None"

    for i, node in enumerate(allocs):
        print(f"{i}: {node}")

    print("Which node do you want to scale down?")

    # TODO: use confirm function
    choice = int(input())

    try:
        node_to_scale_down = allocs[choice][0]
        print(node_to_scale_down)
        return node_to_scale_down
    except IndexError:
        print("Invalid choice")
        return None

def add_constraint_to_job(job_spec, node_to_scale_down):
    """ Add constraint != node_to_scale_down to the job """

    # Modify the job spec
    constraint = {
        "LTarget": "${attr.unique.hostname}",
        "Operand": "!=",
        "RTarget": node_to_scale_down,
    }

    try:
        job_spec["TaskGroups"][0]["Constraints"].append(constraint)
    except AttributeError:
        job_spec["TaskGroups"][0]["Constraints"] = [constraint]

    return job_spec

def get_running_allocations(job_name):
    allocs = get_allocations(job_name)

    return [
        (node, alloc)
        for node, alloc, status in allocs if status == "running"
    ]

def scale_down_job(job_name):
    """ Scale down the job by 1 and returns the node"""

    # Get the current job spec
    job_spec = get_job_spec(job_name)
    allocs = get_running_allocations(job_name)

    node_to_scale_down = ask_which_node_to_scale_down(allocs)

    if node_to_scale_down is None:
        return None

    # Modify the job spec
    scale_down(job_spec)
    add_constraint_to_job(job_spec, node_to_scale_down)

    print(job_spec["TaskGroups"][0]["Constraints"])
    print(job_spec["TaskGroups"][0]["Count"])

    # Ask whether to submit the job_spec
    print("Do you want to submit the job?")
    choice = input()

    # Submit the job
    if choice == "y":
        resp = update_job(job_name, job_spec)
        print(resp.text)
        print(resp.status_code)
        return node_to_scale_down
    else:
        print("Exiting")

if __name__ == "__main__":
    job_name = "hello-world"
    scale_down_job(job_name)
