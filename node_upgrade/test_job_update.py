"""
Tests for nomad job spec update logic
"""

import json
import requests

"""
Test update count of job.group
"""
def test_group_count_update():
    job_name = "hello-world"
    base_url = "https://localhost:4646"
    verify   = False

    # Get the current job spec
    resp = requests.get(base_url + f"/v1/job/{job_name}", verify=verify)
    job_spec = json.loads(resp.text)

    # Modify the job spec
    current_count = job_spec["TaskGroups"][0]["Count"]
    job_spec["TaskGroups"][0]["Count"] += 1

    # Submit the modified job spec
    headers = {"Content-Type": "application/json"}
    resp = requests.post(
        base_url + f"/v1/job/{job_name}",
        headers=headers,
        data=json.dumps({"Job": job_spec}),
        verify=verify,
    )
    assert resp.status_code == 200, resp.text

    # Get the new job spec
    resp = requests.get(base_url + f"/v1/job/{job_name}", verify=verify)
    job_spec = json.loads(resp.text)

    # Assert the change
    assert job_spec["TaskGroups"][0]["Count"] == current_count + 1
