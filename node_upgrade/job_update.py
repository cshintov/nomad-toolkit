"""
Convert the below command into python script.
nomad job inspect hello-world | jq '.Job.TaskGroups[0].Count = 1' | nomad job run -json -
"""

import urllib3
from urllib3 import exceptions
from rich.pretty import pprint as print

from utils import *

urllib3.disable_warnings(exceptions.InsecureRequestWarning)

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
    choice = int(input())

    try:
        node_to_scale_down = allocs[choice][0]
        print(node_to_scale_down)
        return node_to_scale_down
    except IndexError:
        print("Invalid choice")
        ask_which_node_to_scale_down(allocs)

def add_constraint_to_job(job_spec, node_to_scale_down):
    """ Add constraint != node_to_scale_down to the job """

    # Modify the job spec
    constraint = {
        "LTarget": "${attr.unique.hostname}",
        "Operand": "!=",
        "RTarget": node_to_scale_down,
    }

    job_spec["TaskGroups"][0]["Constraints"].append(constraint)
    return job_spec

def get_running_allocations(job_name):
    allocs = get_allocations(job_name)
    return [
        (node, alloc['id'])
        for node, alloc in allocs.items() if alloc['status'] == "running"
    ]

def scale_down_job(job_name):
    """ Scale down the job by 1 """

    # Get the current job spec
    job_spec = get_job_spec(job_name)
    allocs = get_running_allocations(job_name)

    node_to_scale_down = ask_which_node_to_scale_down(allocs)

    # Modify the job spec
    scale_down(job_spec)
    add_constraint_to_job(job_spec, node_to_scale_down)

    print(job_spec)

    # Ask whether to submit the job_spec
    print("Do you want to submit the job?")
    choice = input()

    # Submit the job
    if choice == "y":
        resp = update_job(job_name, job_spec)
        print(resp.text)
        print(resp.status_code)
    else:
        print("Exiting")

if __name__ == "__main__":
    job_name = "hello-world"
    scale_down_job(job_name)
