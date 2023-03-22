# import get_branch_name from upgrade.py

import pytest
from upgrade import *

"""
Getting error. Need to somehow mock it.
"""

def mock_get_branch_name():
    """Mock get_branch_name"""

def test_get_branch_name():
    """Test get_branch_name"""
    assert get_branch_name() == "feature/ALL-899-upgrade-goerli-prysm-to-v3.2.2"

"""
test get_version_from_branch_name
"""
def test_get_version_from_branch_name():
    """Test get_version_from_branch_name"""
    assert get_version_from_branch_name("feature/ALL-899-upgrade-goerli-prysm-to-v3.2.2") == "v3.2.2"
    assert get_version_from_branch_name("feature/ALL-899-upgrade-goerli-geth-to-v1.10.8") == "v1.10.8"

"""
Write a test to verify that the first parameter is the component name and there exists a
dockerfile with that name.
"""

def test_get_image_name_from_dockerfile():
    """Test get_image_name_from_dockerfile"""

    assert get_image_data_from_dockerfile("prysm") == ["gcr.io/prysmaticlabs/prysm/beacon-chain", "v3.2.2"]
    assert get_image_data_from_dockerfile("geth") == ["ethereum/client-go", "v1.11.3"]

"""
Write test to verify that the image exist in dockerhub
"""

@pytest.mark.skip(reason="Need to mock docker cli command")
def test_verify_image_exist_in_dockerhub():
    """Test verify_image_exist_in_dockerhub"""
    assert verify_image_exist_in_dockerhub("ethereum/client-go", "v1.10.8") == True


"""
Write test to verify that the image exist in gcr.io
"""

@pytest.mark.skip(reason="Need to mock gcloud")
def test_verify_image_exist_in_gcr():
    """Test verify_image_exist_in_gcr"""
    assert verify_image_exist_in_gcr("gcr.io/prysmaticlabs/prysm/beacon-chain", "vxx.x.2") == False
    assert verify_image_exist_in_gcr("gcr.io/prysmaticlabs/prysm/beacon-chain", "v3.2.2") == True

"""
Test update_dockerfile
"""


def test_update_the_first_line():
    """Test update_the_first_line"""
    filename = "dummy.Dockerfile"
    new_line = "FROM ethereum/client-go:v1.12.0\n"

    old_content = get_content(filename)

    before = rest_of_the_file(filename)
    update_the_first_line(filename, new_line)
    after = rest_of_the_file(filename)

    assert before == after
    assert first_line(filename) == new_line

    with open(filename, "w") as f:
        f.write(old_content)

def test_update_dockerfile():
    """Test update_dockerfile"""

    component = "dummy"
    upgrade = "v1.13.0"

    old_content = get_content(f"{component}.Dockerfile")

    _, before_version = get_image_data_from_dockerfile(component)
    update_dockerfile(component, upgrade)
    after_version = get_image_data_from_dockerfile(component)[1]

    assert before_version != after_version
    assert after_version == upgrade

    with open(f"{component}.Dockerfile", "w") as f:
        f.write(old_content)
