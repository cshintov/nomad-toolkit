#
#!/bin/bash

# Define the list of nodes with their IP addresses and names
nodes=(
    "51.89.64.18 eu-de1-13"
    "141.95.45.80 eu-de1-01"
    "135.125.160.121 eu-de1-02"
    "135.125.160.122 eu-de1-03"
)

# Define the output file for the table
size_file="chain_sizes.csv"

# Loop through each node and get the size of each directory in /data
for node in "${nodes[@]}"
do
    # Extract the IP address and name of the node
    ip=$(echo $node | cut -d' ' -f1)
    name=$(echo $node | cut -d' ' -f2)

    # Get the list of directories in /data on the node
    dirs=$(ssh $ip zfs list -H -o name | tail -n +2)

    # Loop through each directory and get its estimated size
    for dir in $dirs
    do
        size=$(ssh $ip zfs list -H -o used $dir)

        # Add the directory and its size to the chain sizes file
        echo "$ip,$name,$dir,$size" >> $size_file
    done
done

# Sort the chain sizes file by directory name
sort -t, -k3 $size_file -o $size_file

# Print the chain sizes file to the console
cat $size_file

