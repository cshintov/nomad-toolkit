# read input file
with open('chain_sizes.txt', 'r') as f:
    input_lines = f.readlines()

# create a dictionary to store unique blockchain sizes
blockchain_sizes = {}

# loop over input lines
for line in input_lines:
    # extract blockchain name and size
    blockchain, size = line.strip().split(' - ')
    # check if blockchain already exists in dictionary
    if blockchain in blockchain_sizes:
        # add size to existing blockchain entry
        pass
    else:
        # add new blockchain entry
        blockchain_sizes[blockchain] = float(size[:-3])

# print unique blockchain sizes
print('Unique blockchain sizes:')
for blockchain, size in blockchain_sizes.items():
    unit = 'TB' if size >= 1000 else 'GB'
    size = size / 1000 if unit == 'TB' else int(size)
    print(f'{blockchain} - {size} {unit}')

