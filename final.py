import re

# read data from file
with open('chain_sizes.txt') as f:
    data = f.read()

# extract chain and size information
chain_sizes = re.findall(r'([a-z-]+):\S+ ([\d\.]+) (\w+)B', data)

# print chain and size information in desired format
for chain, size, unit in chain_sizes:
    if unit == 'TB':
        size = f'{float(size):.2f} TB'
    elif unit == 'GB':
        size = f'{float(size):.2f} GB'
    print(f'{chain},{size}')

