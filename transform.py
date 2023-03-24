#!/usr/bin/env python3

# input_file = "/tmp/chain_sizes.csv"
input_file = "filtered.csv"

# dictionary to store the total size of each blockchain
blockchain_sizes = {}

# dictionary to store the number of entries for each blockchain
blockchain_counts = {}

# read input file and calculate total size and counts for each blockchain
# create dictionaries to hold the blockchain sizes and counts
blockchain_sizes = {}
blockchain_counts = {}

# parse input file
with open(input_file, 'r') as f:
    for line in f:
        ip, server, blockchain, size = line.strip().split(',')
        if size[-1] == 'K':
            size = float(size[:-1]) / 1e6
        elif size[-1] == 'M':
            size = float(size[:-1]) / 1e3
        elif size[-1] == 'G':
            size = float(size[:-1])
        elif size[-1] == 'T':
            size = float(size[:-1]) * 1e3
        else:
            raise ValueError(f"Invalid size unit for {line}")

        # update blockchain sizes and counts
        key = f"{server}:{blockchain}"
        blockchain_sizes[key] = blockchain_sizes.get(key, 0) + size
        blockchain_counts[key] = blockchain_counts.get(key, 0) + 1

# calculate average size of each blockchain in TB
blockchain_averages = {}
for blockchain, size in blockchain_sizes.items():
    count = blockchain_counts[blockchain]
    average_size = size / count
    unit = 'GB'
    if average_size < 1:
        average_size *= 1e3
        unit = 'TB'
    # average_size = average_size / 1000
    blockchain_averages[blockchain] = f'{average_size:.2f} {unit}'

# print results
print('Blockchain sizes:')
for blockchain, size in blockchain_averages.items():
    blk = blockchain.split('/')[1]
    print(f'{blk} - {size}')

