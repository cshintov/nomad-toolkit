#!/usr/bin/env python3

# input_file = "/tmp/chain_sizes.csv"
input_file = "chain_sizes.csv"

# dictionary to store the total size of each blockchain
blockchain_sizes = {}

# dictionary to store the number of entries for each blockchain
blockchain_counts = {}

# read input file and calculate total size and counts for each blockchain
with open(input_file) as f:
    for line in f:
        ip, node, blockchain, size = line.strip().split(',')
        size_num = float(size[:-1]) # remove suffix and convert to float
        size_unit = size[-1].upper()
        if size_unit == 'T':
            size_num *= 1000
        elif size_unit == 'G':
            pass
        else:
            # raise ValueError(f'Unknown size unit "{size_unit}" for blockchain "{blockchain}"')
            print(f'Unknown size "{size_num} {size_unit}" for blockchain "{blockchain}" on node "{node}"')

        blockchain_sizes[blockchain] = blockchain_sizes.get(blockchain, 0) + size_num
        blockchain_counts[blockchain] = blockchain_counts.get(blockchain, 0) + 1

# calculate average size of each blockchain in TB or GB
blockchain_averages = {}
for blockchain, size in blockchain_sizes.items():
    count = blockchain_counts[blockchain]
    average_size = size / count
    if average_size >= 1000:
        average_size /= 1000
        unit = 'TB'
    else:
        unit = 'GB'
    blockchain_averages[blockchain] = f'{average_size:.2f} {unit}'

# print results
print('Blockchain sizes:')
for blockchain, size in blockchain_averages.items():
    print(f'{blockchain} - {size}')

