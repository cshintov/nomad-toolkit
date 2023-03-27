"""
Tests for nomad job spec update logic
"""

import time
import json
import requests
import random
import pytest

from job_update import *

job_name = "hello-world"
base_url = "https://localhost:4646"
verify   = False


"""
Test update count of job.group
"""
@pytest.mark.skip(reason="temp")
def test_group_count_update():
    new_count = 5

    job_spec = get_job_spec(job_name)
    job_spec["TaskGroups"][0]["Count"] = new_count

    resp = update_job(job_name, job_spec)

    job_spec = get_job_spec(job_name)
    job_spec["TaskGroups"][0]["Count"] = new_count

    assert resp.status_code == 200

@pytest.mark.skip(reason="temp")
def test_scale_down():
    node_to_remove = ""
    job_spec = get_job_spec(job_name)
    old_count = job_spec["TaskGroups"][0]["Count"]

    if old_count > 1:
        scale_down(job_spec)
        allocs = get_running_allocations(job_name)
        node_to_remove = random.choice(allocs)[0]
        add_constraint_to_job(job_spec, node_to_remove)
        update_job(job_name, job_spec)

    new_job_spec = get_job_spec(job_name)
    count = new_job_spec["TaskGroups"][0]["Count"]

    assert count == old_count - 1

    time.sleep(6)
    assert not node_to_remove in [
        node for (node, _) in get_running_allocations(job_name)
    ]

def test_get_allocations():
    allocs = get_running_allocations(job_name)
    assert len(allocs) == 2
