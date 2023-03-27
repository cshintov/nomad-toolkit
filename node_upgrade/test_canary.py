"""Now we need to add a canary group to the job spec. We can do that by adding
a new task group to the job spec. We can also add a new constraint to the job
which will make the new allocation to be made to the earlier scaled down node.
Also the image to be used in the new task group should be the new image hash.
"""

import time
import pytest
from canary import *
from upgrade import get_target_image
from job_update import get_running_allocations


@pytest.fixture
def job_spec():
    spec = get_job_spec(job_name)

    yield spec

    # print("Revert?")
    # choice = input("y/n: ")
    # if choice == "y":
    resp = update_job(job_name, spec)
    # print(resp.text)
    # print(resp.status_code)
        # time.sleep(15)

# @pytest.mark.skip(reason="Not ready yet")
def test_add_canary_group(job_spec):
    """ Add new task group to the job spec """
    group = job_spec["TaskGroups"][0]["Name"]
    component = "bor"
    task = get_task_name(job_spec["TaskGroups"][0], component)

    target_image = get_target_image(component)

    new_job_spec = copy.deepcopy(job_spec)

    new_task_group = prepare_new_task_group(new_job_spec, target_image, task)
    new_job_spec["TaskGroups"].append(new_task_group)

    resp = update_job(job_name, new_job_spec)
    assert resp.status_code == 200, resp.text

    new_job_spec = get_job_spec(job_name)
    assert len(new_job_spec["TaskGroups"]) == 2

    old_task_group = new_job_spec["TaskGroups"][0]
    assert get_task_name(old_task_group, component) == task
    assert old_task_group["Tasks"][0]["Config"]["image"] != target_image

    new_task_group = new_job_spec["TaskGroups"][1]
    assert new_task_group["Name"] == f"{group}_canary"
    assert get_task_name(new_task_group, component) == f"{task}_canary"
    assert new_task_group["Count"] == 1
    assert new_task_group["Tasks"][0]["Config"]["image"] == target_image

# @pytest.mark.skip(reason="Not ready yet")
def test_prepare_new_task_group():
    job_spec = get_job_spec(job_name)
    group = job_spec["TaskGroups"][0]["Name"]
    component = "bor"
    task = get_task_name(job_spec["TaskGroups"][0], component)

    target_image = get_target_image(component)
    new_task_group = prepare_new_task_group(job_spec, target_image, task)

    assert new_task_group["Name"] == f"{group}_canary"
    assert get_task_name(new_task_group, component) == f"{task}_canary"
    assert new_task_group["Count"] == 1
    assert new_task_group["Tasks"][0]["Config"]["image"] == target_image

@pytest.mark.skip(reason="Slow")
def test_deploy_canary(job_spec):
    """ Test scaling down and deploying canary """
    group = job_spec["TaskGroups"][0]["Name"]
    component = "bor"
    task = get_task_name(job_spec["TaskGroups"][0], component)

    target_image = get_target_image(component)

    # Scale down
    new_job_spec = get_job_spec(job_name)
    new_job_spec["TaskGroups"][0]["Count"] = 1
    resp = update_job(job_name, new_job_spec)
    assert resp.status_code == 200, resp.text

    # Wait for scaling down
    time.sleep(15)

    new_job_spec = copy.deepcopy(job_spec)

    new_task_group = prepare_new_task_group(new_job_spec, target_image, task)
    new_job_spec["TaskGroups"].append(new_task_group)

    resp = update_job(job_name, new_job_spec)
    assert resp.status_code == 200, resp.text

    new_job_spec = get_job_spec(job_name)
    assert len(new_job_spec["TaskGroups"]) == 2

    old_task_group = new_job_spec["TaskGroups"][0]
    assert get_task_name(old_task_group, component) == task
    assert old_task_group["Tasks"][0]["Config"]["image"] != target_image

    new_task_group = new_job_spec["TaskGroups"][1]
    assert new_task_group["Name"] == f"{group}_canary"
    assert get_task_name(new_task_group, component) == f"{task}_canary"
    assert new_task_group["Count"] == 1
    assert new_task_group["Tasks"][0]["Config"]["image"] == target_image

from job_update import scale_down_job

def test_add_canary_on_scaled_down_node(job_spec):
    """ Add new task group to the job spec """
    component = "bor"

    target_image = get_target_image(component)
    scaled_down_node = scale_down_job(job_name)

    spec = get_job_spec(job_name)
    new_job_spec = copy.deepcopy(spec)
    task = get_task_name(spec["TaskGroups"][0], component)

    if len(spec["TaskGroups"]) < 2:
        new_task_group = prepare_new_task_group(job_spec, target_image, task)
        new_job_spec["TaskGroups"].append(new_task_group)
    else:
        new_task_group = copy.deepcopy(spec["TaskGroups"][1])

    # Add constraint to the new task group
    new_task_group["Constraints"].append(
        {
            "LTarget": "${node.unique.name}",
            "Operand": "=",
            "RTarget": f"{scaled_down_node}"
        }
    )

    resp = update_job(job_name, new_job_spec)
    assert resp.status_code == 200, resp.text

    new_job_spec = get_job_spec(job_name)

    new_task_group = new_job_spec["TaskGroups"][1]

    time.sleep(5)

    assert len(get_running_allocations(job_name)) == 2
    assert len(new_job_spec["TaskGroups"]) == 2
    assert new_task_group["Tasks"][0]["Config"]["image"] == target_image

    constraint_exists = any(
        constraint == {
            "LTarget": "${node.unique.name}", 
            "Operand": "=", 
            "RTarget": scaled_down_node
        }
        for constraint in new_task_group["Constraints"]
    )
    assert constraint_exists, f"Constraint not found: {scaled_down_node}"


# def test_workflow():
    # scale_down()
    # add_canary_on_scaled_down_node()
    # deploy_canary()
    # verify_health()
