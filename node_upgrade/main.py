#!/Users/Shinto/.pyenv/shims/python

"""

Automate Blockchain Node Upgrades.

Blockchain node upgrades are hard and it doesn't lend itself to automation
easily. Currently we do this manually, it's error prone - frequently the nodes
get sick after an upgrade - and it's a pain to do repeatedly. This script is a
first step towards automating the upgrade process. It won't be perfect, but it
should be a lot better than what we have now. We won't be able to do this for
all the chains, but we can do it for the ones that are easy to upgrade, for
example `litecoin`.

First step is to update the dockerfile with the new version. We can do this
manually for now, as trying to automate it is a bit tricky. If we standardize
the dockerfiles, we can do it. Simply using the build arguments - ARG in
Dockerfile - everywhere will do the trick.

Our Nomad cluster runs in two regions: EU and US. Mostly we have equal number
of blockchain nodes in both the regions. For some chains we run both the
fullnodes and the archives.

The upgrade process is as follows:

    * Scaled down on one of the nodes in a region, say EU.
    * Take snapshot on that node.
    * Scale it up with canary group using new image.
    * Make sure it's syncing and the health checks are green in Consul.
    * We do this again for the other region.
    * If both are running well, we can raise a PR to update the job spec.
    * And once the PR is accepted and merged, we can rollout the new version to
      all of the nodes.

"""

import sys

import git
from rich.pretty import pprint

from snapshot import take_snapshot

from canary import prepare_canary_group
from utils import confirm, noop, get_job_spec
from image_upgrade import git_commit, git_push, get_commit_hash
from job import (
    get_canary_constraint, deploy, show_changes_to_be_applied, scale_down_job
)

# Be at the root directory of the repo.
REPO = git.Repo('.')
REGISTRY = "registry.gitlab.com/tatum-io/infrastructure"


def commit_and_push(message):
    """ Commit and push the changes to the repo. """
    git_commit(REPO, message)
    git_push(REPO)
    return get_commit_hash(REPO)

def deploy_first_canary(target_image, job, task):
    """ Deploy first canary.

    Get the job spec of the running job. Scale down one of the nodes
    in a region. Take snapshot of the node. Run a canary there.
    """

    prev_job_spec = get_job_spec(job)

    scaled_down_node = scale_down_job(job)
    take_snapshot(scaled_down_node, job)

    current_spec = get_job_spec(job)

    canary_group = prepare_canary_group(prev_job_spec, target_image, task)

    # Add the constraint to the canary group.
    current_spec["TaskGroups"].append(canary_group)
    constraint = get_canary_constraint(canary_group, scaled_down_node)
    constraints = canary_group.get("Constraints", [])
    constraints.append(constraint)

    show_changes_to_be_applied(current_spec)
    status = deploy(job, current_spec)

    return status

def deploy_second_canary(job):
    """ Deploy second canary
    Scale down one of the nodes in the other region.
    Take snapshot of the node. Run a canary there.
    """

    scaled_down_node = scale_down_job(job)
    take_snapshot(scaled_down_node, job)

    # Add to the existing canary group.
    current_spec = get_job_spec(job)
    canary_group = current_spec["TaskGroups"][1]
    constraint = get_canary_constraint(canary_group, scaled_down_node)

    pprint('Adding to existing canary group')
    constraint["RTarget"] += f",{scaled_down_node}"
    current_spec["TaskGroups"][1]["Count"] += 1
    show_changes_to_be_applied(current_spec)
    status = deploy(job, current_spec)

    return status

def upgrade(job, task, version, image, ticket):
    """ Upgrade the job.
    Assumption: Manually updated the dockerfile with the new version.

    Commit and push the changes to the repo.  Deploy first canary.  Deploy
    second canary.
    TODO: If both canaries are running well, raise a PR to update the job spec.
    """

    """
    Confirm that the dockerfile has been manually updated with the new version.
    """
    ok = confirm(
        "Have you updated the dockerfile with the new version?",
        noop
    )

    """ If not we stop here. """
    if not ok:
        print("Please update the dockerfile with the new version.")
        sys.exit(1)

    """ If yes, we commit the change with a comment like
        "ALL-123: Update dockerfile image version to 1.2.3"
    and push it to the repo.
    """
    message = f"{ticket}: Update dockerfile image version to {version}"
    commit_hash = commit_and_push(message)
    print(f"Commit hash: {commit_hash}")

    new_image = f"{REGISTRY}/{image}:{commit_hash}"

    """ We deploy the first canary, and if successful, deploy the second one. """
    ok = deploy_first_canary(new_image, job, task)
    if ok:
        deploy_second_canary(new_image)
    else:
        print("First canary skipped. Exiting.")
        sys.exit(1)

def get_input():
    """Get job, task, version, image, ticket from the user."""
    try:
        job = sys.argv[1]
        task = sys.argv[2]
        version = sys.argv[3]
        image = sys.argv[4]
        ticket = sys.argv[5]
    except IndexError:
        print("Usage: python main.py job task version image ticket")
        sys.exit(1)
    return job, task, version, image, ticket

def main():
    """
    Here we get the `job, task, version, image, ticket` from the user.
    And simply call upgrade function with them.
    """
    job, task, version, image, ticket = get_input()
    upgrade(job, task, version, image, ticket)

if __name__ == "__main__":
    main()
