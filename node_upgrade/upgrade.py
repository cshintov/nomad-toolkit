#!/Users/Shinto/.pyenv/shims/python

"""
Blockchain node upgrades are hard. It's manual, it's error prone, and it's a pain to do repeatedly.
This script is a first step towards automating the upgrade process. It won't be perfect,
but it should be a lot better than what we have now. We won't be able to do this for all
the chains, but we can do it for the ones that are easy to upgrade, for example `litecoin`.

The hardest part is how to modify the nomad job for the things we want to do, for example,
adding a new constraint, or changing the image or adding a canary group.

"""

""""
First let's do the following:
    - get version from branch name
        - the name will be like: `feature/ALL-899-upgrade-goerli-prysm-to-v3.2.2`
    - verify the image exist in dockerhub
        - let's start with this, sometimes we weill have to build the image from binary
    - update image, push, get commit hash
"""

import os
import subprocess
import git

REPO_PATH = '..'

repo = git.Repo(REPO_PATH)

def get_branch_name():
    """Get branch name from git"""
    return os.popen("git branch --show-current").read().strip()

def get_version_from_branch_name(branch_name):
    """Get version from branch name"""
    return branch_name.split("-")[-1]

"""
We can get the image name from the dockerfile.So let's take it as the first
parameter. Let's say we standardize the dockerfile names as
component.Dockerfile. For example, `prysm.Dockerfile` or `geth.Dockerfile`.

Then the first parameter should be the component name, for example `prysm` or
`geth`.
"""

def get_image_data_from_dockerfile(component_name):
    """Get image name from dockerfile"""

    # Read first line of the dockerfile, split based on space and take the
    # second element, will break if it's a multistage dockerfile.
    # TODO: handle multistage dockerfiles
    with open (f"{component_name}.Dockerfile", "r") as dockerfile:
        first_line = dockerfile.readline()
        image = first_line.split(" ")[1].strip()

    # Return the image name and the version
    return image.split(":")

"""
Now we can verify whether the image exist in dockerhub. Combine the image name and the version.
"""

def verify_image_exist_in_dockerhub(image_name, version):
    """Verify image exist in dockerhub"""
    return os.system(f"docker manifest inspect {image_name}:{version} >/dev/null") == 0

""" Tests disabled for now, need to figure out how to mock gcloud. Slow. """
def verify_image_exist_in_gcr(image_name, version):
    """Verify image exist in gcr.io"""
    command = f"""\
        gcloud container images list-tags \
            {image_name} --format='get(tags)' \
            --filter='tags={version}' 2> error.log
    """

    output = subprocess.check_output(command, shell=True)
    return bool(output)

"""
Let's do update image dockerfile, commit, push, get commit hash
"""

def get_content(filename):
    """Get content of file"""
    with open(filename, "r") as file:
        return file.read()

def update_the_first_line(filename, new_line):
    """Update the first line of a file"""
    with open(filename, "r") as file:
        lines = file.readlines()
        lines[0] = new_line
    with open(filename, "w") as file:
        file.writelines(lines)

def first_line(filename):
    """Get the first line of a file"""
    with open(filename, "r") as file:
        return file.readline()

def rest_of_the_file(filename):
    """Get the rest of the file"""
    with open(filename, "r") as file:
        return file.readlines()[1:]

def update_dockerfile(component, new_version):
    """Update dockerfile with new version"""
    current_image, current_version = get_image_data_from_dockerfile(component)

    print(f"Upgrading {component} from {current_version} to {new_version}")

    new_base = f"FROM {current_image}:{new_version}\n"
    update_the_first_line(f"{component}.Dockerfile", new_base)

def git_commit(message):
    """Git commit"""
    repo.git.add(".")
    repo.git.commit(m=message)

def git_push():
    """ Git push to origin with current branch name"""
    repo.git.push("--set-upstream", "origin", get_branch_name())

def get_commit_hash():
    """Git commit hash"""
    return repo.head.object.hexsha

if __name__ == "__main__":
    branch_name = get_branch_name()
    new_version = get_version_from_branch_name(branch_name)
    update_dockerfile("prysm", new_version)
