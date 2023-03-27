import json
import requests

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

def short_id(id):
    return id[:8]

def get_allocations(job_name):
    """ Get allocations of the job """
    resp = requests.get(base_url + f"/v1/job/{job_name}/allocations", verify=verify)

    # Print the allocation ids and nodes (names) they are running on
    return [(
        alloc["NodeName"],
        short_id(alloc["ID"]),
        alloc['ClientStatus']) for alloc in json.loads(resp.text)]


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

def print_json(dict):
    json_string = json.dumps(dict, indent=2)
    print(json_string)

def write_json_to_file(dict, filename):
    with open(filename, "w") as f:
        json.dump(dict, f, indent=2)

