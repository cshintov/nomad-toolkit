"""
The functions here helps to automatically update the version in the Dockerfile.

Not usable at the moment. First we have to standardize the Dockerfile with the use
of build arguments - ARG. Then we can use them to update the Dockerfile.

The git related functions are still used. They are wrappers around gitpython.
"""

import os
import sys
import subprocess

import git

def get_branch_name():
    """Get branch name from git"""
    return os.popen("git branch --show-current").read().strip()

def get_version_from_branch_name(branch_name):
    """Get version from branch name"""
    return branch_name.split("-")[-1]

"""
We can get the image name from the dockerfile. So let's take it as the first
parameter. Let's say we standardize the dockerfile names as
component.Dockerfile. For example, `prysm.Dockerfile` or `geth.Dockerfile`.

Then the first parameter should be the component name, for example `prysm` or
`geth`.
"""

def get_image_data_from_dockerfile(component_name):
    """Get image data from dockerfile"""

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

def get_target_image(component):
    """Get image:tag to be updated to"""
    image, _ = get_image_data_from_dockerfile(component)
    target = get_version_from_branch_name(get_branch_name())
    return f"{image}:{target}"

def update_dockerfile(component, new_version):
    """Update dockerfile with new version"""
    current_image, current_version = get_image_data_from_dockerfile(component)

    print(f"Upgrading {component} from {current_version} to {new_version}")

    new_base = f"FROM {current_image}:{new_version}\n"
    update_the_first_line(f"{component}.Dockerfile", new_base)


# Git related functions

def git_commit(repo, message):
    """Git commit"""
    repo.git.add(".")
    try:
        repo.git.commit(m=message)
    except git.exc.GitCommandError:
        print("Nothing to commit")
        sys.exit(1)

def git_push(repo):
    """ Git push to origin with current branch name"""
    repo.git.push("--set-upstream", "origin", get_branch_name())

def get_commit_hash(repo):
    """Git commit hash"""
    return repo.head.object.hexsha


if __name__ == "__main__":
    branch_name = get_branch_name()
    new_version = get_version_from_branch_name(branch_name)
    update_dockerfile("prysm", new_version)
