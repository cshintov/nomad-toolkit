""" Take snapshot in the scaled down node. """
import os
import paramiko
import datetime
from paramiko.config import SSHConfig

def current_date():
    """Return current date"""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def construct_snapshot_name(chain):
    """ the name of the snapshot will be like `data-pool/<chain>@2023-03-27` """
    date = current_date()
    return f"data-pool/{chain}@{date}"

def connect_to_remote_host(user, host_name):
    """ Connect to remote with host ssh config """
    # Load the SSH configuration options from the config file
    ssh_config = SSHConfig()
    with open(os.path.expanduser('~/.ssh/config')) as f:
        ssh_config.parse(f)

    # Get the configuration options for the target host
    host_config = ssh_config.lookup(host_name)

    # Create a new SSH client object
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote host using the configuration options
    client.connect(
        hostname=host_config['hostname'],
        username=user,
        timeout=10
    )

    return client

def ssh_and_run_command(node_name, command):
    user = "shinto.cv"
    client = connect_to_remote_host(user, node_name)

    _, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()

    if stderr.read().decode():
        print(stderr.read().decode())
        raise Exception("Error while running command")

    client.close()
    return output

def take_snapshot(node_name, dataset):
    """Take snapshot of the dataset"""
    snapshot_name = construct_snapshot_name(dataset)
    command = f"sudo zfs snapshot {snapshot_name}"
    ssh_and_run_command(node_name, command)
