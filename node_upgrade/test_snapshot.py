""" Tests for snapshot 

We need to test the following:
    - Take snapshot in the scaled down node
        - get the node id of the scaled down node
        - get the dataset corresponding to the chain (mainnet, mainnet-archive)
        - the name of the snapshot will be like `data-pool/<chain>@2023-03-27`
        - use zfs list to verify the snapshot is taken
"""

from unittest import mock
import pytest

from snapshot import *

# Ugly. Mocking tests implementation! No time now to setup a proper test
# environment.
@pytest.mark.skip(reason="Ugly.")
def test_ssh_and_run_command():
    """Test running a command on a remote machine"""
    mock_client = mock.Mock()
    mock_stdout = mock.Mock()
    mock_stdout.read.return_value.decode.return_value = 'hello, world!\n'
    mock_client.exec_command.return_value = (mock.Mock(), mock_stdout, mock.Mock())
    mock_client.close.return_value = None
    with mock.patch('paramiko.SSHClient') as mock_ssh_client:
        mock_ssh_client.return_value = mock_client
        # Test running a command on the remote machine
        node_name = 'test-server'
        command = 'echo "hello, world!"'
        output = ssh_and_run_command(node_name, command)
        # Check that the SSH client was called with the correct arguments
        mock_ssh_client.assert_called_once()
        mock_client.set_missing_host_key_policy.assert_called_once_with(mock.ANY)
        mock_client.connect.assert_called_once_with(hostname=node_name, username='shinto.cv', timeout=10)
        mock_client.exec_command.assert_called_once_with(command)
        mock_client.close.assert_called_once()
        # Check that the output is correct
        assert output == 'hello, world!\n'

def test_current_date():
    """Test current date"""
    assert current_date() == "2023-03-27"

def test_construct_snapshot_name():
    """Test construct snapshot name"""
    assert (
        construct_snapshot_name("mainnet") == "data-pool/mainnet@2023-03-27")
    assert (
        construct_snapshot_name("mainnet-archive") 
        == "data-pool/mainnet-archive@2023-03-27"
    )

def snapshot_exists(node_name, dataset):
    """Check if snapshot exists"""
    snapshot_name = construct_snapshot_name(dataset)
    command = f"zfs list -t snapshot | grep {snapshot_name}"
    output = ssh_and_run_command(node_name, command)
    return output != ""

def test_take_snapshot():
    node_name = "eu-de1-01"
    dataset = "mycoin-testnet"

    take_snapshot(node_name, dataset)
    assert snapshot_exists(node_name, dataset)

    # Remove the snapshot
    snapshot_name = construct_snapshot_name(dataset)
    command = f"sudo zfs destroy {snapshot_name}"
    ssh_and_run_command(node_name, command)
    assert not snapshot_exists(node_name, dataset)
