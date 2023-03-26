"""
We don't have to add a variable. We can't. It's not part of the job spec.
We can handle it in the script. Get the new image hash. Get the current image from the spec.
Replace just the tag with the new image hash. Update the image in the spec. Submit.
"""

def update_image(job_spec, new_image_hash):
    pass

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
