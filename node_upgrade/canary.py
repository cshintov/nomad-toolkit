"""
We don't have to add a variable. We can't. It's not part of the job spec.
We can handle it in the script. Get the new image hash. Get the current image from the spec.
Replace just the tag with the new image hash. Update the image in the spec. Submit.
"""

import copy
from utils import *

# TODO: Adding constraint for the canary
# TODO: Add a function to get the diff between the current job spec and the new job spec
# TODO: What if there are multiple tasks for the same component?
# like erigon? the node and the rpc server?

"""Now we need to add a canary group to the job spec. We can do that by adding
a new task group to the job spec. We can also add a new constraint to the job
which will make the new allocation to be made to the earlier scaled down node.
Also the image to be used in the new task group should be the new image hash.
"""

def get_task_name(task_group, component):
    """ Get the name of the task. """
    target_task = get_target_task(task_group, component)
    return target_task["Name"]

def get_target_task(task_groups, task_name):
    """ Get the task. We will have to loop through
    the tasks in the task group and get the task by filtering
    for the component specified.
    """
    target_task = {}
    for task in task_groups["Tasks"]:
        if task_name == task["Name"]:
            target_task = task
            break

    return target_task

def prepare_canary_group(job_spec, target_image, task_name):
    """ Prepare new task group by copying the existing task group
    and modifying the name, count and image.
    """
    group = job_spec["TaskGroups"][0]
    task = get_target_task(group, task_name)

    # Deepcopy the existing task group and prepare.
    new_group = copy.deepcopy(group)
    new_group["Name"] = f"{group['Name']}_canary"
    new_group["Count"] = 1

    # Set the upgraded image to the canary task config.
    task["Config"]["image"] = target_image

    return new_group

