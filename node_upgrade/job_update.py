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

def get_job_spec(job_name):
    resp = requests.get(base_url + f"/v1/job/{job_name}", verify=verify)
    job_spec = json.loads(resp.text)
    return job_spec

def update_count(count, job_spec):
    job_spec["TaskGroups"][0]["Count"] = count
    return job_spec

def scale_up(job_spec):
    count = job_spec["TaskGroups"][0]["Count"]
    update_count(count + 1, job_spec)

def scale_down(job_spec):
    count = job_spec["TaskGroups"][0]["Count"]
    update_count(count - 1, job_spec)

def print_json(dict):
    json_string = json.dumps(dict, indent=2)
    print(json_string)

def write_json_to_file(dict, filename):
    with open(filename, "w") as f:
        json.dump(dict, f, indent=2)

"""
We don't have to add a variable. We can't. It's not part of the job spec.
We can handle it in the script. Get the new image hash. Get the current image from the spec.
Replace just the tag with the new image hash. Update the image in the spec. Submit.
"""

def update_image(job_spec, new_image_hash):
    pass


"""
Before this we have to handle the scale down of the job. Then add new canary
group. Only then we can update the image.
"""

def short_id(id):
    return id[:8]

def get_allocations(job_name):
    """ Get allocations of the job """
    resp = requests.get(base_url + f"/v1/job/{job_name}/allocations", verify=verify)

    # Print the allocation ids and nodes (names) they are running on
    allocs = {}
    for alloc in json.loads(resp.text):
        allocs[alloc["NodeName"]] = {
            'id': short_id(alloc["ID"]),
            'status': alloc['ClientStatus']
        }

    return allocs

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

def update_job(job_name, job_spec):
    """Submit the modified job spec"""

    headers = {"Content-Type": "application/json"}
    resp = requests.post(
        base_url + f"/v1/job/{job_name}",
        headers=headers,
        data=json.dumps({"Job": job_spec}),
        verify=verify,
    )
    return resp

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

# TODO: Add a function to get the diff between the current job spec and the new job spec

"""Now we need to add a canary group to the job spec. We can do that by adding
a new task group to the job spec. We can also add a new constraint to the job
which will make the new allocation to be made to the earlier scaled down node.
Also the image to be used in the new task group should be the new image hash.
"""

# def add_canary_group(job_spec, new_image_hash):
    # """ Add new task group to the job spec """
    # new_task_group = prepare_new_task_group(job_spec, new_image_hash)

    # job_spec["TaskGroups"].append(new_task_group)
#     return job_spec

# scale_down_job(job_name)
