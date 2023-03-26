"""
Tests for nomad job spec update logic
"""

import json
import requests

from job_update import *

job_name = "hello-world"
base_url = "https://localhost:4646"
verify   = False


"""
Test update count of job.group
"""
def test_group_count_update():
    new_count = 2

    job_spec = get_job_spec(job_name)
    job_spec["TaskGroups"][0]["Count"] = new_count

    resp = update_job(job_name, job_spec)

    job_spec = get_job_spec(job_name)
    job_spec["TaskGroups"][0]["Count"] = new_count

    assert resp.status_code == 200
