#
#!/bin/bash

# Define the list of nodes with their IP addresses and names
nodes=(
    "51.89.64.67 eu-de1-app01"
    "51.89.64.18 eu-de1-app02"
    "51.89.64.18 eu-de1-13"
    "141.95.45.80 eu-de1-01"
    "135.125.160.121 eu-de1-02"
    "135.125.160.122 eu-de1-03"
    "141.95.34.120 eu-de1-04"
    "141.95.33.43 eu-de1-05"
    "141.95.45.190 eu-de1-06"
    "141.95.45.187 eu-de1-07"
    "141.95.45.56 eu-de1-08"
    "162.19.136.25 eu-de1-09"
    "162.19.136.66 eu-de1-10"
    "162.19.136.65 eu-de1-11"
    "162.19.136.216 eu-de1-12"
    "51.89.64.18 eu-de1-13"
    "51.89.64.67 eu-de1-14"
    "51.195.63.10 eu-de1-15"
    "162.19.168.181 eu-de1-16"
    "162.19.138.4 eu-de1-17"
    "51.83.220.97 eu-lb2"
    "51.81.184.9 us-west1-01"
    "51.81.184.85 us-west1-02"
    "51.81.154.19 us-west1-03"
    "51.81.185.218 us-west1-04"
    "51.81.185.219 us-west1-05"
    "51.81.185.220 us-west1-06"
    "51.81.185.221 us-west1-07"
    "51.81.184.18 us-west1-08"
    "51.81.244.140 us-west1-09"
    "51.81.244.144 us-west1-10"
    "51.81.244.143 us-west1-11"
    "51.81.244.142 us-west1-12"
    "51.81.184.86 us-west1-13"
    "51.81.184.88 us-west1-14"
    "51.81.184.92 us-west1-15"
    "51.81.184.90 us-west1-16"
    "51.81.184.91 us-west1-17"
    "51.81.184.89 us-west1-18"
    "51.81.184.87 us-west1-19"
    "51.81.184.130 us-west1-20"
    "51.81.184.148 us-west1-21"
)
#nodes=(
    #"51.89.64.18 eu-de1-13"
    #"141.95.45.80 eu-de1-01"
    #"135.125.160.121 eu-de1-02"
    #"135.125.160.122 eu-de1-03"
#)

# Define the output file for the table
size_file="chain_sizes.csv"
user="shinto.cv"

# Loop through each node and get the size of each directory in /data
for node in "${nodes[@]}"
do
    # Extract the IP address and name of the node
    ip=$(echo $node | cut -d' ' -f1)
    name=$(echo $node | cut -d' ' -f2)
    echo "Processing: $name"

    # Get the list of directories in /data on the node
    dirs=$(ssh "$user@$ip" zfs list -H -o name | tail -n +2)

    # Loop through each directory and get its estimated size
    # Get the list of directories and sizes from the mock data file
    for dir in $dirs
    do
        size=$(ssh "$user@$ip" zfs list -H -o used $dir)

        # Add the directory and its size to the chain sizes file
        echo "$ip,$name,$dir,$size" >> $size_file
    done
done

# Sort the chain sizes file by directory name
sort -t, -k3 $size_file -o $size_file

# Print the chain sizes file to the console
cat $size_file

