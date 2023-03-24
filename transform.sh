#!/bin/bash

# Define the input file
input_file="/tmp/chain_sizes.csv"

# Declare an associative array to store the blockchain sizes
declare -g -A blockchain_sizes

# Loop through each line in the input file and extract the blockchain name and size
while read -r line
do
    # Extract the IP address, blockchain name, and size from the line
    ip=$(echo "$line" | awk -F',' '{print $1}')
    name=$(echo "$line" | awk -F',' '{print $3}')
    size=$(echo "$line" | awk -F',' '{print $4}')

    # Remove the "T" suffix from the size and convert it to a float
    size=$(echo "$size" | sed 's/T//g')
    size=$(echo "$size/1000" | bc)

    # Add the size to the blockchain_sizes array
    if [[ ${blockchain_sizes[$name]+_} ]]
    then
        blockchain_sizes[$name]=$(echo "scale=2; (${blockchain_sizes[$name]} + $size) / 2" | bc)
    else
        blockchain_sizes[$name]=$size
    fi
done < "$input_file"

# Print the blockchain sizes
echo "Blockchain Sizes (TB):"
for blockchain in "${!blockchain_sizes[@]}"
do
    size=${blockchain_sizes[$blockchain]}
    echo "$blockchain - $(printf "%.2f" "$size") TB"
done

