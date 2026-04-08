import json
from eth_utils import keccak, to_checksum_address

def get_leaf(address):
    return keccak(bytes.fromhex(to_checksum_address(address)[2:]))

def build_tree(leaves):
    nodes = sorted(leaves)
    while len(nodes) > 1:
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])
        nodes = [keccak(nodes[i] + nodes[i+1]) for i in range(0, len(nodes), 2)]
    return nodes[0]

with open('addresses.txt', 'r') as f:
    addresses = [line.strip() for line in f if line.strip()]

leaves = [get_leaf(addr) for addr in addresses]
root = build_tree(leaves)

print(f"DONE! Processed {len(addresses)} addresses.")
print(f"Merkle Root: 0x{root.hex()}")