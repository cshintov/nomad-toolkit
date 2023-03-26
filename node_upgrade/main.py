"""
This script is used to upgrade nomad job task image.

First we need to scaled down on one of the nodes in the region.
Take snapshot on the node. Then scale backup the job with canary group.
The canary group will make use of the new image.
We do this again for the other region.
If both are running well, we can raise a PR to update the job spec.
"""

from upgrade import upgrade

if __name__ == "__main__":
    job = "hello-world"
    task = "hello"
    upgrade(job, task)
